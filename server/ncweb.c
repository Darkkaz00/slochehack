#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void unescape(char *);

#define myBUFSIZ (5 * 1024)
#define TOKS 2000

/* small buffer sizes to test the overflow prevention system */

/*
	define myBUFSIZ 1024
	define TOKS 100
*/

int unsafe(char* s){
	while(*s){
		if(! (isalnum(*s) || *s=='.' || *s=='_' || *s=='/'))	return 1;
		++s;
	}
	return 0;
}

int unsafe_2(char* s){
	while(*s){
		if(! (isalnum(*s) || *s=='.' || *s==' ' || *s=='\n' || *s=='\r'))	return 1;
		++s;
	}
	return 0;
}

void footer()
{
	fflush(stdout);
	printf("<P><HR><FONT SIZE='-1'><I>The &quot;Clown&quot; WebServer<BR><a href='/'>index</a> <a href='/about'>about</a>");
}

int main(int argc, char** argv)
{
	FILE* clownbuf = NULL;
	char buf[myBUFSIZ + 1024];
	char tmp[myBUFSIZ + 1024];
	char tmp2[myBUFSIZ + 1024];
	char tmp3[myBUFSIZ + 1024];
	char* ptmp;
	char* tokens[TOKS];
	int i, j, k;
	char* p;
	int cl;
	char* ptr;
	FILE* log = fopen("log.txt", "a");

	while(!feof(stdin)) {
		fgets(buf, myBUFSIZ, stdin);
		fprintf(log, "GOT %s\n", buf);

		/* tokenize stdin buffer */
		i = 0;
		p = buf;
		j = 0;
		k = 1;

		while(*p) {
			if(++j > myBUFSIZ)	goto hack_attempt;

			if(*p != ' ' && *p != '\n' && *p != '\r'){
				if(k) {
					tokens[i] = p;
					k = 0;
				}			
			} else {
				*p = 0;
				k = 1;
				i++;
				if(i > TOKS)	goto hack_attempt;
			}
			p++;
		}

		if(i < 2) goto hack_attempt;

		if(strlen(tokens[2]) > strlen("HTTP/1.23456789")) goto hack_attempt2;

		/*
		 * for(j = 0; j < i; j++)	printf("token %d : '%s'\n", j, tokens[j]);
		 */

		if(!strcmp(tokens[0], "GET")){
			printf("%s 200 OK\n", tokens[2]);
			fflush(stdout);

			/* Decor salle privees liposuccion (v4 2006-2007) */
			if (strstr(tokens[1], "/client/decor/lipo_decor.swf")) {
				printf("\n");
				fflush(stdout);
				system("cat sloche-data/0.swf");
				fflush(stdout);
			}

			/* GOT GET /client/decor/22.swf HTTP/1.1 */
			if(strstr(tokens[1], "/client/decor/")){
				printf("\n");
				fflush(stdout);
				sprintf(tmp, "cat sloche-data/%s", tokens[1] + strlen("/client/decor"));
				system(tmp);
				fflush(stdout);
			}

			if(!strcmp(tokens[1], "/client/popup.html")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/popup.html");
				fflush(stdout);
			}

			if(!strcmp(tokens[1], "/")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/index.html");
				fflush(stdout);
			}

			if(!strcmp(tokens[1], "/splahtml.gif")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/splahtml.gif");
				fflush(stdout);
			}

			if(!strcmp(tokens[1], "/client/son/son1.swf")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/1.swf");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/client/son/son2.swf")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/2.swf");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/client/son/son3.swf")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/3.swf");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/client/son/son4.swf")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/4.swf");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/client/son/son5.swf")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/5.swf");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/client/son/son6.swf")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/6.swf");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/client/sloche.swf")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/sloche.swf");
				fflush(stdout);
			}

			if(!strcmp(tokens[1], "/swompe/pouvoirs.txt")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/pouvoirs.txt");
				fflush(stdout);
			}

			/* /swompe/pouvoirs/images/ico/24.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/24.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-telep.jpg");
				fflush(stdout);
			}

			/* 23 -> icone-vip.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/23.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-vip.jpg");
				fflush(stdout);
			}

			/* 26 -> icone-vip.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/26.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-nouveaux-persos.jpg");
				fflush(stdout);
			}

			/* 31 -> icone-pet.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/31.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-pet.jpg");
				fflush(stdout);
			}

			/* 12 -> icone-laser.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/12.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-laser.jpg");
				fflush(stdout);
			}

			/* 13 -> icone-mouche.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/13.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-mouche.jpg");
				fflush(stdout);
			}

			/* 25 -> icone-mini.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/25.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-mini.jpg");
				fflush(stdout);
			}

			/* 21 -> icone-scie.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/21.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-scie.jpg");
				fflush(stdout);
			}


			/* 14 -> icone-wribit.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/14.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-wribit.jpg");
				fflush(stdout);
			}

			/* 22 -> icone-barbu.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/22.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-barbu.jpg");
				fflush(stdout);
			}

			/* 32 -> icone-velo.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/32.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-velo.jpg");
				fflush(stdout);
			}

			/* 33 -> icone-ultra.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/33.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-ultra.jpg");
				fflush(stdout);
			}

			/* 41 -> icone-real.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/41.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-real.jpg");
				fflush(stdout);
			}

			/* 27 -> icone-rrdb.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/27.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-rrdb.jpg");
				fflush(stdout);
			}

			/* 11 -> icone-geant.jpg */
			if(!strcmp(tokens[1], "/swompe/pouvoirs/images/ico/11.jpg")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/icone-geant.jpg");
				fflush(stdout);
			}

			if(!strcmp(tokens[1], "/client/simpleChatConfig.xml")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/simpleChatConfig.xml");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/client/simpleChatConfig1.xml")){
				printf("\n");
				fflush(stdout);	
				system("cat sloche-data/simpleChatConfig.xml");
				fflush(stdout);
			}
			if(!strcmp(tokens[1], "/crossdomain.xml")){
				/*
					Error: [strict] Ignoring policy file
					at http://admin.sloche.com/crossdomain
					.xml due to missing Content-Type.
				*/
				printf("Content-Type: text/xml\n\n");
				fflush(stdout);	
				system("cat sloche-data/crossdomain.xml");
				fflush(stdout);
			}

			goto close_connection;
		}

		if(!strcmp(tokens[0], "POST")) {
			printf("%s 200 OK\n", tokens[2]);

			if (!strcmp(tokens[1], "/usagers/psw.sn")) {
				cl = 0;
				while(!feof(stdin)){
					fgets(buf, myBUFSIZ, stdin);
					fprintf(log, "POST:  %s", buf);
					fflush(log);
					if(strstr(buf, "Content-Length:"))	sscanf(buf, "Content-Length: %d", &cl);
					if(strstr(buf, "Content-length:"))	sscanf(buf, "Content-length: %d", &cl);	/* >:( */
					if(strstr(buf, "content-length:"))	sscanf(buf, "content-length: %d", &cl);	/* >:( */
					if(strlen(buf) < 3){
						fgets(buf, cl ? cl + 1: myBUFSIZ, stdin);
						fprintf(log, "Content: '%s'\n", buf);
						fflush(log);
						break;
					}
				}

				sprintf(tmp, "cd ../xml-server/; python psw2004.py \"%s\"; cd ../server/", buf);

				printf("\n");
				fflush(stdout);	
				system(tmp);
				fflush(stdout);
			}

			if (!strcmp(tokens[1], "/membres/liste")) {
				cl = 0;
				while(!feof(stdin)){
					fgets(buf, myBUFSIZ, stdin);
					fprintf(log, "POST:  %s", buf);
					fflush(log);
					if(strstr(buf, "Content-Length:"))	sscanf(buf, "Content-Length: %d", &cl);
					if(strstr(buf, "Content-length:"))	sscanf(buf, "Content-length: %d", &cl);	/* >:( */
					if(strstr(buf, "content-length:"))	sscanf(buf, "content-length: %d", &cl);	/* >:( */
					if(strlen(buf) < 3){
						fgets(buf, cl ? cl + 1: myBUFSIZ, stdin);
						fprintf(log, "Content: '%s'\n", buf);
						fflush(log);
						break;
					}
				}

				sprintf(tmp, "cd ../xml-server/; python fiche.py \"%s\"; cd ../server/", buf);

				printf("\n");
				fflush(stdout);	
				system(tmp);
				fflush(stdout);
			}

			if(!strcmp(tokens[1], "/inscriptions")){
				cl = 0;
				while(!feof(stdin)){
					fgets(buf, myBUFSIZ, stdin);
					fprintf(log, "POST:  %s", buf);
					fflush(log);
					if(strstr(buf, "Content-Length:"))	sscanf(buf, "Content-Length: %d", &cl);
					if(strstr(buf, "Content-length:"))	sscanf(buf, "Content-length: %d", &cl);	/* >:( */
					if(strstr(buf, "content-length:"))	sscanf(buf, "content-length: %d", &cl);	/* >:( */
					if(strlen(buf) < 3){
						fgets(buf, cl ? cl + 1: myBUFSIZ, stdin);
						fprintf(log, "Content: '%s'\n", buf);
						fflush(log);
						break;
					}
				}

				sprintf(tmp, "cd ../xml-server/; python get_user.py \"%s\"; cd ../server/", buf);

				printf("\n");
				fflush(stdout);	
				system(tmp);
				fflush(stdout);
			} else if(!strcmp(tokens[1], "/usagers/mapage.sn")) {
				cl = 0;
				while(!feof(stdin)){
					fgets(buf, myBUFSIZ, stdin);
					fprintf(log, "POST:  %s", buf);
					fflush(log);
					if(strstr(buf, "Content-Length:"))	sscanf(buf, "Content-Length: %d", &cl);
					if(strstr(buf, "Content-length:"))	sscanf(buf, "Content-length: %d", &cl);	/* >:( */
					if(strstr(buf, "content-length:"))	sscanf(buf, "content-length: %d", &cl);	/* >:( */
					if(strlen(buf) < 3){
						fgets(buf, cl ? cl + 1: myBUFSIZ, stdin);
						fprintf(log, "Content: '%s'\n", buf);
						fflush(log);
						break;
					}
				}

				sprintf(tmp, "cd ../xml-server/; python update_user.py \"%s\"; cd ../server/", buf);
				printf("\n");
				fflush(stdout);	
				system(tmp);
				printf("\n");
				fflush(stdout);

			} else if(!strcmp(tokens[1], "/usagers/inscriptions.sn")){
				cl = 0;
				while(!feof(stdin)){
					fgets(buf, myBUFSIZ, stdin);
					fprintf(log, "POST:  %s", buf);
					fflush(log);
					if(strstr(buf, "Content-Length:"))	sscanf(buf, "Content-Length: %d", &cl);
					if(strstr(buf, "Content-length:"))	sscanf(buf, "Content-length: %d", &cl);	/* >:( */
					if(strstr(buf, "content-length:"))	sscanf(buf, "content-length: %d", &cl);	/* >:( */
					if(strlen(buf) < 3){
						fgets(buf, cl ? cl + 1: myBUFSIZ, stdin);
						fprintf(log, "Content: '%s'\n", buf);
						fflush(log);
						break;
					}
				}

				sprintf(tmp, "cd ../xml-server/; python new_user.py \"%s\"; cd ../server/", buf);
				printf("\n");
				fflush(stdout);	
				system(tmp);
				printf("\n");
				fflush(stdout);
			} else if(!strcmp(tokens[1], "/courriel/liste")){
				printf("\n");
				fflush(stdout);
				printf(" &nb=0& \n");
				fflush(stdout);
			} else if(!strcmp(tokens[1], "/swompe/pouvoirs/liste.sn")){

				cl = 0;
				while(!feof(stdin)){
					fgets(buf, myBUFSIZ, stdin);
					fprintf(log, "POST:  %s", buf);
					fflush(log);
					if(strstr(buf, "Content-Length:"))	sscanf(buf, "Content-Length: %d", &cl);
					if(strstr(buf, "Content-length:"))	sscanf(buf, "Content-length: %d", &cl);	/* >:( */
					if(strstr(buf, "content-length:"))	sscanf(buf, "content-length: %d", &cl);	/* >:( */
					if(strlen(buf) < 3){
						fgets(buf, cl ? cl + 1: myBUFSIZ, stdin);
						fprintf(log, "Content: '%s'\n", buf);
						fflush(log);
						break;
					}
				}
				printf("\n");
				fflush(stdout);

				system("cat liste-pouvoirs.txt");
				printf("\n");
				fflush(stdout);


			} else {

				printf("\n\n");	fflush(stdout);
			}

			goto close_connection;
		}

		fflush(stdout);
	}

	if(feof(stdin)) {
		fprintf(log, "CONNECTION CLOSED BY CLIENT\n");
	}

	if(0){
		hack_attempt:
		printf("\n");
		fflush(stdout);
		printf("<HTML>\n<H1>Overflow</H1>");
		printf("You overflowed my server's buffers with this request, sorry. \n");
		printf("<BR>Back to <a href='/'>index</a> page\n</HTML>");
		fflush(stdout);
	}

	if(0){
		hack_attempt2:
		printf("\n");
		fflush(stdout);
		printf("<HTML>\n<H1>Malformed or dubious request</H1>");
		printf("This request looks strange.\n");
		printf("<BR>Back to <a href='/'>index</a> page\n</HTML>");
		fflush(stdout);
	}

	close_connection:

	fprintf(log, "CLOSING SERVER\n");

	fflush(stdout);
	//printf("\n\n");

	fclose(log);

	return 0;
}

/*
 * e.g. "%23%21/usr/bin/clown%20hahah%20@%25%21%3F"
 * becomes "#!/usr/bin/clown hahah @%!?"
 */

void unescape(char* str){
	char* buf = malloc(strlen(str));
	char* p = str;
	char* o = buf;
	unsigned int c;

	if(!buf) return;

	while(*p){
		if(*p == '%'){
			sscanf(++p, "%2x", &c);
			++p;
			*(o++) = (char)c;	
		} else if(*p == '+')
			*(o++) = ' ';	/* >:( */
		else	*(o++) = *p;
		++p;
	}
	
	*o = '\0';
	
	sprintf(str, "%s", buf);
	free(buf);	
}


