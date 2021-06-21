/******************************************************************************
* The tokenizer for FlexJSON
# /home/git/external/SAS_NA1_3D_Spectrograph/docs/source/images/flexjson.l
* flex flexjson.l && ls
* flex flexjson.l  && g++ -c lex.yy.c && g++ -o playlex lex.yy.o  && ./playlex playlexinput.txt 
*****************************************************************************/

%{
/* need this for the call to atof() below */
#include <iostream>
#include <string>
using namespace std;

int yywrap() {return 1;}

%}

%%

[0-9]+                    { yy.lval = yytext ; return INTEGER;    }
[0-9]+[.][0-9]*           { yy.lval = yytext ; return FLOAT;      }
[A-Za-z0-9_][A-Za-z0-9_]* { yy.lval = yytext ; return STRING;     }
[{]                       { yy.lval = yytext ; return OPENBRACE;  }
[}]                       { yy.lval = yytext ; return CLOSEBRACE; }
["]                       { yy.lval = yytext ; return QUOTE;      }
[,]                       { yy.lval = yytext ; return COMMA;      }
[:]                       { yy.lval = yytext ; return COLON;      }
\n                        /*IGNORE*/ ;
[ 	]                     /*IGNORE  NOTE: Hidden tab in the rule*/ ;

%%

#ifdef __REGRESSION__
int main(int argc, char **argv )
{
    ++argv, --argc;  /* skip over program name */
    if ( argc > 0 )
            yyin = fopen( argv[0], "r" );
    else
            yyin = stdin;

    yylex();
    return 0;

} // Main
#ENDIF

