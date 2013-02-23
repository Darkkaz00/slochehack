/*
 * Ce fichier est une version légèrement modifiée
 * du fichier exemple dlg_three.c donné par theForger
 * sur son site http://www.winprog.org/tutorial/
 *
 * Il y a aussi des bouts copiés d'autres exemples
 * provenant de la même archive.
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "resource.h"

char buf[1024];		/* usage général */
FILE *f;

int fichier_ok = 0;	/* choix fichier client OK ? */
int version = 0;	/* 1: version 2003, 2: version 2004-2007 */
char pwd[4096];		/* directoire slochehack */

char fichier[MAX_PATH] = "";	/* chemin fichier client */
char adr[256] = "";			/* addresse IP */

HBRUSH g_hbrBackground = NULL;
OPENFILENAME ofn;
char szFileName[MAX_PATH] = "";

void ecrire_comme_du_monde(char *str, FILE* f)
{
	char *p;

	for (p = str; *p; ++p)
		if (*p != '\n')
			fputc(*p, f);

	fputc('\n', f);
}

char * enlever_lignes(char *str)
{
	static char buf[4096];
	char *p = str;
	char *q = &buf[0];
	while (*p) {
		if (*p != '\n')
			*q++ = *p;
		++p;
	}
	*q = 0;
	return buf;
}

int check_flasm()
{
	/* http://stackoverflow.com/questions/3828835/how-can-we-check-if-a-file-exists-or-not-using-win32-program */

	/* aller dans la directoire principale slochehack */
	SetCurrentDirectory(pwd);

	return GetFileAttributes("flasm.exe") != 0xFFFFFFFF;
}

BOOL CALLBACK DlgProc(HWND hwnd, UINT Message, WPARAM wParam, LPARAM lParam)
{
	switch(Message)
	{
		case WM_INITDIALOG:
			/* stocker la directoire de lancement pour usage futur */
			GetCurrentDirectory(4096, pwd);

			/* sauvegarde ? */
			if ((f = fopen("config_slochehack.txt", "r"))) {
				fgets(fichier, MAX_PATH, f);
				fgets(adr, 256, f);
				fgets(buf, 1024, f);
				fclose(f);
				sscanf(buf, "%d", &version);

				SetDlgItemText(hwnd, IDC_EDIT1, fichier);
				SetDlgItemText(hwnd, IDC_EDIT2, adr);
				fichier_ok = 1;

				if (version == 1)
					SendMessage(GetDlgItem(hwnd, IDC_RADIO1), BM_SETCHECK, BST_CHECKED,1);
				if (version == 2)
					SendMessage(GetDlgItem(hwnd, IDC_RADIO2), BM_SETCHECK, BST_CHECKED,1);
			}

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

				case IDC_BUTTON4:	/* bouton "sauvegarder" */
				/* aller dans la directoire principale slochehack */
				SetCurrentDirectory(pwd);

					if ((f = fopen("config_slochehack.txt", "w"))) {
						GetWindowText(GetDlgItem(hwnd, IDC_EDIT1), fichier, MAX_PATH);
						ecrire_comme_du_monde(fichier, f);

						GetWindowText(GetDlgItem(hwnd, IDC_EDIT2), adr, 256);
						ecrire_comme_du_monde(adr, f);

						sprintf(buf, "%d", version);
						ecrire_comme_du_monde(buf, f);

						fclose(f);
					} else {
						MessageBox(hwnd, "Echec de la sauvegarde",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					}
					break;

				case IDC_BUTTON3:	/* bouton "regarder ipconfig" */
					system("start cmd.exe /kipconfig");
					break;

				case IDC_BUTTON2:	/* bouton "lancer le serveur" */
					/* aller chercher l'addresse IP choisie */
					GetWindowText(GetDlgItem(hwnd, IDC_EDIT2), adr, 256);

					/* chercher fichier client */
					GetWindowText(GetDlgItem(hwnd, IDC_EDIT1), fichier, MAX_PATH);

					if (strlen(adr) < 2) {
						MessageBox(hwnd, "SVP choisir une addresse IP de serveur",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);				
					}
					else if (strlen(fichier) < 2) {
						MessageBox(hwnd, "SVP choisir un fichier client",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					} else if (!check_flasm()) {
						MessageBox(hwnd, "SVP copier flasm.exe dans le dossier slochehack",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					} else if (!version) {
						MessageBox(hwnd, "SVP choisir une version du client", "Erreur", 
							MB_OK | MB_ICONEXCLAMATION);
					}
					else {
						/* aller dans la directoire principale slochehack */
						SetCurrentDirectory(pwd);

						/* lancer la première partie du serveur */
						sprintf(buf, "start lancement1.bat ");
						strcat(buf,  enlever_lignes(adr));
						strcat(buf, " \"");
						strcat(buf, enlever_lignes(fichier));
						strcat(buf, "\"");
						system(buf);

						if (version == 1)
							sprintf(buf, "start lancement2003.bat ");
						else
							sprintf(buf, "start lancement2.bat ");
						strcat(buf,  enlever_lignes(adr));
						strcat(buf, " \"");
						strcat(buf, enlever_lignes(fichier));
						strcat(buf, "\"");

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
						if (strlen(szFileName)) {
							fichier_ok = 1;
							strcpy(fichier, szFileName);
							SetDlgItemText(hwnd, IDC_EDIT1, fichier);
						}
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