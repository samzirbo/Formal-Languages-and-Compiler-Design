%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yyerror(char *s);
extern int yylex(void);

#define YYDEBUG 1 
%}

%token INT
%token CONST
%token STR
%token LIST
%token OF
%token IF
%token THEN
%token ELSE
%token WHILE
%token FOR
%token IN
%token NOT
%token DO
%token END
%token AND
%token OR

%token PLUS
%token MINUS
%token MULTIPLY
%token DIVISION
%token MODULO
%token EQUAL
%token LESS_THAN
%token LESS_OR_EQUAL_THAN
%token GREATER_THAN
%token GREATER_OR_EQUAL_THAN
%token DOUBLE_EQUAL
%token NOT_EQUAL
%token SHIFT_LEFT
%token SHIFT_RIGHT

%token LEFT_ROUND_PARENTHESIS
%token RIGHT_ROUND_PARENTHESIS
%token DOT
%token COMMA
%token COLON
%token LEFT_CURLY_BRACE
%token RIGHT_CURLY_BRACE
%token LEFT_SQUARE_BRACKET
%token RIGHT_SQUARE_BRACKET

%token ID

%start program

%%

program: statement_list
statement_list: statement | statement statement_list
statement: declaration | assignment | io | if_stmt | while_stmt | for_stmt

expression: term | term PLUS expression | term MINUS expression
term: factor | factor MULTIPLY term | factor DIVISION term | factor MODULO term
factor: ID | CONST | ID LEFT_SQUARE_BRACKET expression RIGHT_SQUARE_BRACKET | LEFT_ROUND_PARENTHESIS expression RIGHT_ROUND_PARENTHESIS

type: primitive | array_decl
primitive: INT | STR
array_decl: LIST OF primitive

declaration: ID COLON type | ID_list COLON type
ID_list: ID | ID COMMA ID_list

assignment: ID EQUAL expression

io: SHIFT_RIGHT expression | SHIFT_LEFT expression

if_stmt: IF LEFT_ROUND_PARENTHESIS condition RIGHT_ROUND_PARENTHESIS THEN statement_list END | IF LEFT_ROUND_PARENTHESIS condition RIGHT_ROUND_PARENTHESIS THEN statement_list ELSE statement_list END

while_stmt: WHILE LEFT_ROUND_PARENTHESIS condition RIGHT_ROUND_PARENTHESIS DO statement_list END

for_stmt: FOR for_header DO statement_list END
for_header: ID IN ID | ID IN LEFT_CURLY_BRACE expression RIGHT_CURLY_BRACE | ID IN LEFT_CURLY_BRACE expression COLON expression RIGHT_CURLY_BRACE | ID IN LEFT_CURLY_BRACE expression COLON expression COLON expression RIGHT_CURLY_BRACE

condition: expression relation expression
relation: DOUBLE_EQUAL | NOT_EQUAL | LESS_THAN | LESS_OR_EQUAL_THAN | GREATER_THAN | GREATER_OR_EQUAL_THAN

%%

yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;
extern int yylex(void);

main(int argc, char **argv)
{
  if(argc>1) yyin = fopen(argv[1], "r");
  if((argc>2)&&(!strcmp(argv[2],"-d"))) yydebug = 1;
  if(!yyparse()) fprintf(stderr,"\t Correct syntax!\n");
}
