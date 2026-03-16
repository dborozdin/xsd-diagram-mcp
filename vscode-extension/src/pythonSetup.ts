import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { execFile } from 'child_process';
import { promisify } from 'util';
import { getConfig } from './config';
import { PIP_PACKAGE, VENV_DIR_NAME, INSTALL_MARKER } from './constants';

const execFileAsync = promisify(execFile);

function getVenvPython(venvDir: string): string {
    return process.platform === 'win32'
        ? path.join(venvDir, 'Scripts', 'python.exe')
        : path.join(venvDir, 'bin', 'python');
}

async function findPython(): Promise<string> {
    const { pythonPath } = getConfig();
    if (pythonPath) {
        return pythonPath;
    }

    const candidates = process.platform === 'win32'
        ? ['python', 'python3']
        : ['python3', 'python'];

    for (const cmd of candidates) {
        try {
            const { stdout } = await execFileAsync(cmd, ['--version']);
            if (stdout.includes('Python 3')) {
                return cmd;
            }
        } catch {
            // try next
        }
    }

    throw new Error(
        'Python 3.10+ not found. Install Python and reload VS Code, ' +
        'or set "xsdDiagramMcp.pythonPath" in settings.'
    );
}

async function verifyPythonVersion(pythonPath: string): Promise<void> {
    const { stdout } = await execFileAsync(pythonPath, [
        '-c', 'import sys; print(sys.version_info.major, sys.version_info.minor)',
    ]);
    const [major, minor] = stdout.trim().split(' ').map(Number);
    if (major < 3 || (major === 3 && minor < 10)) {
        throw new Error(
            `Python 3.10+ is required, but found ${major}.${minor}. ` +
            'Update Python or set "xsdDiagramMcp.pythonPath" to a compatible version.'
        );
    }
}

export async function ensurePythonEnvironment(
    context: vscode.ExtensionContext,
    outputChannel: vscode.OutputChannel,
): Promise<string> {
    const pythonPath = await findPython();
    await verifyPythonVersion(pythonPath);

    const storageDir = context.globalStorageUri.fsPath;
    if (!fs.existsSync(storageDir)) {
        fs.mkdirSync(storageDir, { recursive: true });
    }

    const venvDir = path.join(storageDir, VENV_DIR_NAME);
    const venvPython = getVenvPython(venvDir);

    if (!fs.existsSync(venvPython)) {
        outputChannel.appendLine(`Creating virtual environment at ${venvDir}...`);
        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'XSD Diagram MCP: Creating Python environment...',
                cancellable: false,
            },
            async () => {
                await execFileAsync(pythonPath, ['-m', 'venv', venvDir]);
            },
        );
    }

    const markerFile = path.join(venvDir, INSTALL_MARKER);
    if (!fs.existsSync(markerFile)) {
        outputChannel.appendLine('Installing xsd-diagram-mcp package...');
        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'XSD Diagram MCP: Installing dependencies (this may take a minute)...',
                cancellable: false,
            },
            async () => {
                const { stdout, stderr } = await execFileAsync(
                    venvPython,
                    ['-m', 'pip', 'install', '--upgrade', PIP_PACKAGE],
                    { timeout: 300_000 },
                );
                outputChannel.appendLine(stdout);
                if (stderr) {
                    outputChannel.appendLine(stderr);
                }
            },
        );
        fs.writeFileSync(markerFile, new Date().toISOString());
        outputChannel.appendLine('Installation complete.');
    }

    return venvPython;
}

export async function cleanEnvironment(context: vscode.ExtensionContext): Promise<void> {
    const venvDir = path.join(context.globalStorageUri.fsPath, VENV_DIR_NAME);
    if (fs.existsSync(venvDir)) {
        fs.rmSync(venvDir, { recursive: true, force: true });
    }
}
