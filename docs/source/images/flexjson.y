%{
#include <string>
#include <iostream>
using namespace std;

void yyerror(const char *str)
{
        cerr << "error:" << str << endl;
}
 
int yywrap()
{
        return 1;
} 
  
main()
{
        yyparse();
} 

%}

%token OPENBRACE
%token CLOSEBRACE
%token COMMA
%token COLON
%token QUOTE
%token STRING
%token INTEGER
%token FLOAT

%%
    
    FlexJSON     : Dictionay
                 ;
    
    Dictionay    : OPENBRACE KeyValueList CLOSEBRACE
                 ;
    
    KeyValueList : KeyValue
                 |  KeyValueList COMMA KeyValue
                 ;
    
    KeyValue     : Key COLON Value
                 ;
    
    Key          : QUOTE STRING QUOTE
    
    Value        : String
                 |  INTEGER
                 |  FLOAT
                 |  Dictionay
                 ;
    
    String       : QUOTE STRING QUOTE
                 ;
