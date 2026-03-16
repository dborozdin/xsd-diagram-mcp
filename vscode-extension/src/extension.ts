import * as vscode from 'vscode';
import { ensurePythonEnvironment, cleanEnvironment } from './pythonSetup';
import { PROVIDER_ID, SERVER_LABEL } from './constants';

export async function activate(context: vscode.ExtensionContext) {
    const outputChannel = vscode.window.createOutputChannel('XSD Diagram MCP');
    context.subscriptions.push(outputChannel);

    const provider = vscode.lm.registerMcpServerDefinitionProvider(
        PROVIDER_ID,
        {
            provideMcpServerDefinitions: async () => {
                try {
                    const pythonPath = await ensurePythonEnvironment(context, outputChannel);
                    return [
                        {
                            type: 'stdio',
                            label: SERVER_LABEL,
                            command: pythonPath,
                            args: ['-m', 'xsd_diagram_mcp.server'],
                        } satisfies vscode.McpStdioServerDefinition,
                    ];
                } catch (err: unknown) {
                    const message = err instanceof Error ? err.message : String(err);
                    outputChannel.appendLine(`Error: ${message}`);
                    vscode.window.showWarningMessage(
                        `XSD Diagram MCP: ${message}`,
                    );
                    return [];
                }
            },
        },
    );
    context.subscriptions.push(provider);

    const reinstallCmd = vscode.commands.registerCommand(
        'xsdDiagramMcp.reinstall',
        async () => {
            outputChannel.appendLine('Reinstalling Python environment...');
            await cleanEnvironment(context);
            vscode.window.showInformationMessage(
                'XSD Diagram MCP: Environment removed. Reload window to reinstall.',
            );
        },
    );
    context.subscriptions.push(reinstallCmd);
}

export function deactivate() {}
