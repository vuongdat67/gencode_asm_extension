// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

const INFER_URL = 'http://127.0.0.1:9137/infer';

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

async function fetchCandidates(payload: { source: string; similarity: string; var_map: Record<string, unknown> }): Promise<Candidate[]> {
	const response = await fetch(INFER_URL, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	});

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

export function activate(context: vscode.ExtensionContext) {
	const disposable = vscode.commands.registerCommand('asm-suggest.insertAsm', async () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.window.showWarningMessage('No active editor to insert ASM suggestion.');
			return;
		}

		const selection = editor.selection;
		const selectedText = editor.document.getText(selection).trim();
		if (!selectedText) {
			vscode.window.showWarningMessage('Select source text to send to the ASM daemon.');
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

		const stripComment = (line: string) => line.replace(/^\s*(;|\/\/|#)\s*/, '');

		if (lines.length === 1) {
			const cleaned = stripComment(lines[0]);
			const payload = {
				source: cleaned,
				similarity: cleaned || lines[0],
				var_map: {},
			};

			const candidates = await vscode.window.withProgress<Candidate[]>({
				location: vscode.ProgressLocation.Notification,
				title: 'Fetching ASM suggestions...',
				cancellable: false,
			}, async () => fetchCandidates(payload));

			const quickItems = candidates.map((candidate, index) => ({
				label: index === 0 ? 'Best ASM suggestion' : `Alternative ${index}`,
				detail: candidate.reason,
				description: candidate.score !== undefined ? `score: ${candidate.score.toFixed(3)}` : undefined,
				candidate,
			}));

			const choice = candidates.length > 1
				? await vscode.window.showQuickPick(quickItems, {
					ignoreFocusOut: true,
					placeHolder: 'Pick an ASM suggestion to insert',
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

			vscode.window.showInformationMessage('ASM suggestion inserted.');
			return;
		}

		const assembled: string[] = [];
		await vscode.window.withProgress<void>({
			location: vscode.ProgressLocation.Notification,
			title: 'Fetching ASM suggestions for multiple lines...',
			cancellable: false,
		}, async (progress) => {
			for (let i = 0; i < lines.length; i += 1) {
				const cleaned = stripComment(lines[i]);
				const payload = {
					source: cleaned,
					similarity: cleaned || lines[i],
					var_map: {},
				};

				progress.report({ message: `Line ${i + 1}/${lines.length}` });
				const candidates = await fetchCandidates(payload);
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

		vscode.window.showInformationMessage(`Inserted ${assembled.length} ASM lines.`);
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
