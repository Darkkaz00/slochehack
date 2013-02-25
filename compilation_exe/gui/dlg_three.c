/*
 * Ce fichier est une version légèrement modifiée
 * du fichier exemple dlg_three.c donné par theForger
 * sur son site http://www.winprog.org/tutorial/
 *
 * Il y a aussi des bouts copiés d'autres exemples
 * provenant de la même archive, et encore des
 * bouts copiés d'exemples donnés sur Internet.
 * Je suis pas un expert de programmation Windows
 * et je n'ai ni le temps ni l'envie d'en devenir
 * un, alors je n'ai pas de honte à faire du
 * copier-coller-modifier.
 *
 * Le fichier ressources a été modifié à l'aide
 * du logiciel ResEdit.
 *
 * - Gabriel
 * 24 février 2013
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "resource.h"

char buf[1024];		/* Usage général */
FILE *f;		/* Usage général */

int version = 0;	/* 1: version 2003, 2: version 2004-2007 */
char pwd[4096];		/* Directoire principale slochehack */

char fichier[MAX_PATH] = "";	/* Chemin fichier client choisi */
char adr[256] = "";		/* Addresse IP serveur choisie */

/* Variables de programmation Windows tirées
 * de l'exemple fourni par theForger */
HBRUSH g_hbrBackground = NULL;
OPENFILENAME ofn;
char szFileName[MAX_PATH] = "";

/*
 * Écrire une chaîne de caractères dans un fichier,
 * en n'y écrivant pas les caractères "newline"
 */
void ecrire_comme_du_monde(char *str, FILE* f)
{
	char *p;

	for (p = str; *p; ++p)
		if (*p != '\n')
			fputc(*p, f);

	fputc('\n', f);
}

/*
 * Enlever les caractères "newline" d'une chaîne
 * de caractères. Attention: ça retourne une seule
 * et unique chaine en stockage "automatique".
 */
char* enlever_lignes(char *str)
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

/*
 * Vérifier si le programme "flasm.exe" est bel
 * et bien présent dans la directoire principale
 * du logiciel.
 */
int check_flasm()
{
	/* Aller dans la directoire principale slochehack */
	SetCurrentDirectory(pwd);

	/* http://stackoverflow.com/questions/3828835/how-can-we-check-if-a-file-exists-or-not-using-win32-program */
	return GetFileAttributes("flasm.exe") != 0xFFFFFFFF;
}

int check_decor()
{
	/* Aller dans la directoire principale slochehack */
	SetCurrentDirectory(pwd);

	/* http://stackoverflow.com/questions/3828835/how-can-we-check-if-a-file-exists-or-not-using-win32-program */
	return GetFileAttributes("server\\sloche-data\\11.swf") != 0xFFFFFFFF;
}

/* La routine principale de la fenêtre graphique */
BOOL CALLBACK DlgProc(HWND hwnd, UINT Message, WPARAM wParam, LPARAM lParam)
{
	switch(Message)
	{
		case WM_INITDIALOG:
			/* Stocker la directoire de lancement pour usage futur */
			GetCurrentDirectory(4096, pwd);

			/* Charger fichier sauvegarde, s'il y a lieu */
			if ((f = fopen("config_slochehack.txt", "r"))) {
				fgets(fichier, MAX_PATH, f);
				fgets(adr, 256, f);
				fgets(buf, 1024, f);
				fclose(f);
				sscanf(buf, "%d", &version);

				/* Remplir les champs de la fenêtre avec les
				 * valeurs sauvegardées */
				SetDlgItemText(hwnd, IDC_EDIT1, fichier);
				SetDlgItemText(hwnd, IDC_EDIT2, adr);

				/* Cocher version sauvegardée choisie */
				if (version == 1)
					SendMessage(GetDlgItem(hwnd, IDC_RADIO1), BM_SETCHECK, BST_CHECKED,1);
				if (version == 2)
					SendMessage(GetDlgItem(hwnd, IDC_RADIO2), BM_SETCHECK, BST_CHECKED,1);
			}

			/* Formalités directement copiées de l'exemple de theForger */
			SendMessage(hwnd, WM_SETICON, ICON_SMALL, (LPARAM)LoadIcon(NULL,
				MAKEINTRESOURCE(IDI_APPLICATION)));
			SendMessage(hwnd, WM_SETICON, ICON_BIG, (LPARAM)LoadIcon(NULL,
				MAKEINTRESOURCE(IDI_APPLICATION)));
		break;

		/* Encore d'autre formalités copiées */

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

		/* Les boutons, à présent */
		case WM_COMMAND:
			switch(LOWORD(wParam))
			{
				case IDC_RADIO1:	/* Choix client 2003 */
					version = 1;
					break;

				case IDC_RADIO2:	/* Choix client 2004-2007 */
					version = 2;
					break;

				case IDC_BUTTON4:	/* Bouton "sauvegarder" */
					/* Aller dans la directoire principale slochehack */
					SetCurrentDirectory(pwd);

					/* Tenter d'ouvrir le fichier de sauvegarde et
					 * y écrire comme du monde les données */
					if ((f = fopen("config_slochehack.txt", "w"))) {
						/* fichier client choisi */
						GetWindowText(GetDlgItem(hwnd, IDC_EDIT1), fichier, MAX_PATH);
						ecrire_comme_du_monde(fichier, f);

						/* addresse IP choisie */
						GetWindowText(GetDlgItem(hwnd, IDC_EDIT2), adr, 256);
						ecrire_comme_du_monde(adr, f);

						/* version du client */
						sprintf(buf, "%d", version);
						ecrire_comme_du_monde(buf, f);

						fclose(f);
					} else {
						MessageBox(hwnd, "Échec de la sauvegarde",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					}
					break;

				case IDC_BUTTON3:	/* Bouton "regarder ipconfig" */
					system("start cmd.exe /kipconfig");
					break;

				case IDC_BUTTON2:	/* Bouton "lancer le serveur" */
					/* Aller chercher l'addresse IP choisie */
					GetWindowText(GetDlgItem(hwnd, IDC_EDIT2), adr, 256);

					/* Chercher chemin fichier client */
					GetWindowText(GetDlgItem(hwnd, IDC_EDIT1), fichier, MAX_PATH);

					if (strlen(adr) < 2) {
						MessageBox(hwnd, "SVP choisir une addresse IP de serveur",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					} else if (strlen(fichier) < 2) {
						MessageBox(hwnd, "SVP choisir un fichier client",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					} else if (!check_flasm()) {
						MessageBox(hwnd, "SVP copier flasm.exe dans le dossier slochehack",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					} else if (!version) {
						MessageBox(hwnd, "SVP choisir une version du client",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					} else if (!check_decor()) {
						MessageBox(hwnd, "11.swf est absent... SVP copier les decors au bons endroits. voir FICHIERS-EXTERNES-REQUIS.TXT",
							"Erreur", MB_OK | MB_ICONEXCLAMATION);
					}
					else {
						/* Lancer la première partie du serveur
						 * (modifications XML et SWF, serveur web) */
						sprintf(buf, "start lancement1.bat ");
						strcat(buf,  enlever_lignes(adr));
						strcat(buf, " \"");
						strcat(buf, enlever_lignes(fichier));
						strcat(buf, "\"");

						/* Lancer la commande dans la directoire principale */
						SetCurrentDirectory(pwd);
						system(buf);

						/* Lancer la deuxième partie, soit le serveur
						 * de messages XML */
						if (version == 1)
							sprintf(buf, "start lancement2003.bat ");
						else
							sprintf(buf, "start lancement2.bat ");
						strcat(buf,  enlever_lignes(adr));
						strcat(buf, " \"");
						strcat(buf, enlever_lignes(fichier));
						strcat(buf, "\"");

						/* Lancer la commande dans la directoire principale */
						SetCurrentDirectory(pwd);
						system(buf);
					}
					break;

				case IDC_BUTTON1:	/* Parcourir pour choisir fichier client */
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
							strcpy(fichier, szFileName);
							SetDlgItemText(hwnd, IDC_EDIT1, fichier);
						}
					}
				break;

				case IDOK:			/* Quitter */
					EndDialog(hwnd, 0);
				break;
			}
		break;

		/* Formalités */

		case WM_DESTROY:
			DeleteObject(g_hbrBackground);
		break;

		default:
			return FALSE;
	}
	return TRUE;
}

/* Entrée */
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
	LPSTR lpCmdLine, int nCmdShow)
{
	return DialogBox(hInstance, MAKEINTRESOURCE(IDD_MAIN), NULL, DlgProc);
}

