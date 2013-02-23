/*
 * Ce fichier est une version legerement modifiee
 * du fichier exemple dlg_three.c donne par theForger
 * sur son site http://www.winprog.org/tutorial/
 * 
 * Il y a aussi des bouts copies d'autres exemples
 * provenant de la meme archive.
 */

#include <windows.h>

#include "resource.h" 

int fichier_ok = 0;
int version = 0;
int ip_ok = 0;
char buf[1024];
char pwd[4096];

HBRUSH g_hbrBackground = NULL;
OPENFILENAME ofn;
char szFileName[MAX_PATH] = "";
char adr[256] = "";

BOOL CALLBACK DlgProc(HWND hwnd, UINT Message, WPARAM wParam, LPARAM lParam)
{
	switch(Message)
	{
		case WM_INITDIALOG:
			GetCurrentDirectory(4096, pwd);
			SendMessage(hwnd, WM_SETICON, ICON_SMALL, (LPARAM)LoadIcon(NULL, 
				MAKEINTRESOURCE(IDI_APPLICATION)));
			SendMessage(hwnd, WM_SETICON, ICON_BIG, (LPARAM)LoadIcon(NULL, 
				MAKEINTRESOURCE(IDI_APPLICATION)));
		break;
		case WM_CLOSE:
			EndDialog(hwnd, 0);
		break;
		case WM_CTLCOLORDLG:	
			return (LONG)g_hbrBackground;
		case WM_CTLCOLORSTATIC:
		{
			HDC hdcStatic = (HDC)wParam;
			SetTextColor(hdcStatic, RGB(255, 255, 255));
			SetBkMode(hdcStatic, TRANSPARENT);
			return (LONG)g_hbrBackground;
		}
		break;
		case WM_COMMAND:
			switch(LOWORD(wParam))
			{
				case IDC_RADIO1:	/* choix client 2003 */
					version = 1;
					break;

				case IDC_RADIO2:	/* choix client 2004-2007 */
					version = 2;
					break;

				case IDC_BUTTON2:	/* bouton "lancer le serveur" */
					if (!version) {
						MessageBox(hwnd, "SVP choisir une version du client", "Erreur", 
							MB_OK | MB_ICONEXCLAMATION);
					}
					else if (!fichier_ok) {
						MessageBox(hwnd, "SVP choisir un fichier client", "Erreur", 
							MB_OK | MB_ICONEXCLAMATION);
					}
					else {
						GetWindowText(GetDlgItem(hwnd, IDC_EDIT2), adr, 256);
						// szFileName		adr

						SetCurrentDirectory(pwd);

						sprintf(buf, "start lancement1.bat %s \"%s\"", adr, szFileName);
						system(buf);						

						SetCurrentDirectory(pwd);

						if (version == 1) {
							sprintf(buf, "start lancement2003.bat %s \"%s\"", adr, szFileName);
						} else {
							sprintf(buf, "start lancement2.bat %s \"%s\"", adr, szFileName);
						}
						system(buf);
					}
					break;

				case IDC_BUTTON1:	/* parcourir pour choisir fichier client */
	ZeroMemory(&ofn, sizeof(ofn));
	ofn.lStructSize = sizeof(ofn);
	ofn.hwndOwner = hwnd;
	ofn.lpstrFilter = "Fichiers Flash (*.swf)\0*.swf\0Tous les fichiers (*.*)\0*.*\0";
	ofn.lpstrFile = szFileName;
	ofn.nMaxFile = MAX_PATH;
	ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;
	ofn.lpstrDefExt = "swf";

	if(GetOpenFileName(&ofn)) {
		SetDlgItemText(hwnd, IDC_EDIT1, szFileName);
		if (strlen(szFileName))
			fichier_ok = 1;
	}
					break;

				case IDOK:			/* quitter */
					EndDialog(hwnd, 0);
				break;
			}
		break;
		case WM_DESTROY:
			DeleteObject(g_hbrBackground);
		break;
		default:
			return FALSE;
	}
	return TRUE;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
	LPSTR lpCmdLine, int nCmdShow)
{
	return DialogBox(hInstance, MAKEINTRESOURCE(IDD_MAIN), NULL, DlgProc);
}
