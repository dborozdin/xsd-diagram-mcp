import * as vscode from 'vscode';

export function getConfig() {
    const config = vscode.workspace.getConfiguration('xsdDiagramMcp');
    return {
        pythonPath: config.get<string>('pythonPath', ''),
        lang: config.get<string>('lang', ''),
    };
}
