/*
 * Ce fichier est une version légèrement modifiée
 * du fichier exemple dlg_three.c donné par theForger
 * sur son site http://www.winprog.org/tutorial/
 *
 * Il y a aussi des bouts copiés d'autres exemples
 * provenant de la même archive.
 */

#include <windows.h>

#include "resource.h"

char buf[1024];		/* usage général */

int fichier_ok = 0;	/* choix fichier client OK ? */
int version = 0;	/* 1: version 2003, 2: version 2004-2007 */
char pwd[4096];		/* directoire slochehack */

HBRUSH g_hbrBackground = NULL;
OPENFILENAME ofn;
char szFileName[MAX_PATH] = "";		/* chemin fichier client */
char adr[256] = "";			/* addresse IP */

BOOL CALLBACK DlgProc(HWND hwnd, UINT Message, WPARAM wParam, LPARAM lParam)
{
	switch(Message)
	{
		case WM_INITDIALOG:
			/* stocker la directoire de lancement pour usage futur */
			GetCurrentDirectory(4096, pwd);

			/* formalités directement copiées de l'exemple de theForger */
			SendMessage(hwnd, WM_SETICON, ICON_SMALL, (LPARAM)LoadIcon(NULL, 
				MAKEINTRESOURCE(IDI_APPLICATION)));
			SendMessage(hwnd, WM_SETICON, ICON_BIG, (LPARAM)LoadIcon(NULL, 
				MAKEINTRESOURCE(IDI_APPLICATION)));
		break;

		/* encore d'autre formalités copiées */

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

		/* les boutons, à présent */

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
						/* aller chercher l'addresse IP choisie */
						GetWindowText(GetDlgItem(hwnd, IDC_EDIT2), adr, 256);

						sprintf(buf, "start lancement1.bat %s \"%s\"", adr, szFileName);
						/* aller dans la directoire principale slochehack */
						SetCurrentDirectory(pwd);
						/* lancer la première partie du serveur */
						system(buf);

						if (version == 1) {
							sprintf(buf, "start lancement2003.bat %s \"%s\"", adr, szFileName);
						} else {
							sprintf(buf, "start lancement2.bat %s \"%s\"", adr, szFileName);
						}
						SetCurrentDirectory(pwd); /* directoire principale */
						system(buf);			/* lancement partie 2 */
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

		/* formalités */

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
