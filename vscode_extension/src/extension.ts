// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

const DEFAULT_INFER_URL = 'http://127.0.0.1:9138/infer';

type Candidate = {
	text: string;
	score?: number;
	reason?: string;
};

function normalizeCandidates(payload: unknown): Candidate[] {
	if (!payload) {
		return [];
	}

	// Common shapes: { best: string, alternatives: string[] } or arrays of strings/objects.
	if (Array.isArray(payload)) {
		return payload
			.map((item) => {
				if (typeof item === 'string') {
					return { text: item } as Candidate;
				}
				if (item && typeof item === 'object' && 'text' in item) {
					const candidate = item as { text?: unknown; score?: unknown; reason?: unknown };
					return {
						text: typeof candidate.text === 'string' ? candidate.text : '',
						score: typeof candidate.score === 'number' ? candidate.score : undefined,
						reason: typeof candidate.reason === 'string' ? candidate.reason : undefined,
					};
				}
				return { text: '' } as Candidate;
			})
			.filter((c) => c.text);
	}

	if (typeof payload === 'object' && payload !== null) {
		const bag = payload as Record<string, unknown>;
		const fromBest = bag.best;
		const fromCandidates = bag.candidates || bag.alternatives;
		const collected: Candidate[] = [];

		if (typeof fromBest === 'string') {
			collected.push({ text: fromBest });
		}
		if (fromBest && typeof fromBest === 'object' && 'text' in (fromBest as Record<string, unknown>)) {
			const bestObj = fromBest as { text?: unknown; score?: unknown; reason?: unknown };
			collected.push({
				text: typeof bestObj.text === 'string' ? bestObj.text : '',
				score: typeof bestObj.score === 'number' ? bestObj.score : undefined,
				reason: typeof bestObj.reason === 'string' ? bestObj.reason : undefined,
			});
		}

		if (Array.isArray(fromCandidates)) {
			collected.push(...normalizeCandidates(fromCandidates));
		}

		return collected.filter((c) => c.text);
	}

	return [];
}

async function fetchCandidates(
	payload: { source: string; similarity: string; var_map: Record<string, unknown> },
	inferUrl: string,
): Promise<Candidate[]> {
	let response: Response;
	try {
		response = await fetch(inferUrl, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(payload),
		});
	} catch (err) {
		throw new Error(`Fetch failed to ${inferUrl}: ${String(err)}`);
	}

	const text = await response.text();
	if (!response.ok) {
		throw new Error(`Daemon returned ${response.status} ${response.statusText}: ${text}`);
	}

	let data: unknown;
	try {
		data = JSON.parse(text);
	} catch (err) {
		throw new Error(`Failed to parse daemon JSON: ${String(err)}. Body: ${text}`);
	}

	const normalized = normalizeCandidates(data);
	if (!normalized.length) {
		throw new Error('Daemon response did not contain any suggestions.');
	}
	return normalized;
}

function getInferUrl(): string {
	const config = vscode.workspace.getConfiguration('asmSuggest');
	const url = config.get<string>('inferUrl')?.trim();
	return url && url.length > 0 ? url : DEFAULT_INFER_URL;
}

function getEndpoints(): string[] {
	const config = vscode.workspace.getConfiguration('asmSuggest');
	const endpoints = config.get<string[]>('endpoints') || [];
	const normalized = endpoints
		.map((u) => (typeof u === 'string' ? u.trim() : ''))
		.filter((u) => u.length > 0);
	return normalized.length ? normalized : [DEFAULT_INFER_URL];
}

async function switchEndpoint(): Promise<void> {
	const endpoints = getEndpoints();
	const pick = await vscode.window.showQuickPick(
		endpoints.map((u) => ({ label: u })),
		{ placeHolder: 'Chọn endpoint daemon (ASM/Python)', ignoreFocusOut: true },
	);
	if (!pick) {
		return;
	}
	const config = vscode.workspace.getConfiguration('asmSuggest');
	await config.update('inferUrl', pick.label, vscode.ConfigurationTarget.Global);
	vscode.window.showInformationMessage(`asmSuggest.inferUrl set to ${pick.label}`);
}

export function activate(context: vscode.ExtensionContext) {
	const output = vscode.window.createOutputChannel('ASM Suggest');

	const disposable = vscode.commands.registerCommand('asm-suggest.insertAsm', async () => {
		try {
			const editor = vscode.window.activeTextEditor;
			if (!editor) {
				vscode.window.showWarningMessage('No active editor to insert suggestion.');
				return;
			}

			const selection = editor.selection;
			const selectedText = editor.document.getText(selection).trim();
			if (!selectedText) {
				vscode.window.showWarningMessage('Select source text to send to the daemon.');
				return;
			}

			const lines = selectedText
				.split(/\r?\n/)
				.map((line) => line.trim())
				.filter((line) => line.length > 0);
			if (!lines.length) {
				vscode.window.showWarningMessage('Selection is empty after trimming.');
				return;
			}

			const inferUrl = getInferUrl();
			output.appendLine(`[infer] url=${inferUrl}`);
			const stripComment = (line: string) => line.replace(/^\s*(;|\/\/|#)\s*/, '');

			if (lines.length === 1) {
				const cleaned = stripComment(lines[0]);
				output.appendLine(`[req] single source='${cleaned}'`);
				const payload = {
					source: cleaned,
					similarity: cleaned || lines[0],
					var_map: {},
				};

				const candidates = await vscode.window.withProgress<Candidate[]>({
					location: vscode.ProgressLocation.Notification,
					title: 'Fetching suggestions...',
					cancellable: false,
				}, async () => fetchCandidates(payload, inferUrl));
				output.appendLine(`[resp] got ${candidates.length} candidates`);

				const quickItems = candidates.map((candidate, index) => ({
					label: index === 0 ? 'Best suggestion' : `Alternative ${index}`,
					detail: candidate.reason,
					description: candidate.score !== undefined ? `score: ${candidate.score.toFixed(3)}` : undefined,
					candidate,
				}));

				const choice = candidates.length > 1
					? await vscode.window.showQuickPick(quickItems, {
						ignoreFocusOut: true,
						placeHolder: 'Pick a suggestion to insert',
					})
					: quickItems[0];

				const selectedCandidate = choice?.candidate ?? candidates[0];
				const insertText = selectedCandidate.text;

				await editor.edit((editBuilder) => {
					if (selection.isEmpty) {
						editBuilder.insert(selection.active, insertText);
					} else {
						editBuilder.replace(selection, insertText);
					}
				});

				vscode.window.showInformationMessage('Suggestion inserted.');
				return;
			}

			const assembled: string[] = [];
			await vscode.window.withProgress<void>({
				location: vscode.ProgressLocation.Notification,
				title: 'Fetching suggestions for multiple lines...',
				cancellable: false,
			}, async (progress) => {
				for (let i = 0; i < lines.length; i += 1) {
					const cleaned = stripComment(lines[i]);
					output.appendLine(`[req] line ${i + 1}/${lines.length} source='${cleaned}'`);
					const payload = {
						source: cleaned,
						similarity: cleaned || lines[i],
						var_map: {},
					};

					progress.report({ message: `Line ${i + 1}/${lines.length}` });
					const candidates = await fetchCandidates(payload, inferUrl);
					assembled.push(candidates[0].text);
				}
			});

			const insertText = assembled.join('\n');
			await editor.edit((editBuilder) => {
				if (selection.isEmpty) {
					editBuilder.insert(selection.active, insertText);
				} else {
					editBuilder.replace(selection, insertText);
				}
			});

			vscode.window.showInformationMessage(`Inserted ${assembled.length} lines.`);
		} catch (err) {
			const msg = `ASM Suggest failed: ${String(err)}`;
			output.appendLine(msg);
			vscode.window.showErrorMessage(msg);
		}
	});

	const switchCmd = vscode.commands.registerCommand('asm-suggest.switchEndpoint', async () => {
		try {
			await switchEndpoint();
		} catch (err) {
			vscode.window.showErrorMessage(`Switch endpoint failed: ${String(err)}`);
		}
	});

	context.subscriptions.push(disposable);
	context.subscriptions.push(switchCmd);
}

export function deactivate() {}
