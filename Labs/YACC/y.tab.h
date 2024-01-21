/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     INT = 258,
     CONST = 259,
     STR = 260,
     LIST = 261,
     OF = 262,
     IF = 263,
     THEN = 264,
     ELSE = 265,
     WHILE = 266,
     FOR = 267,
     IN = 268,
     NOT = 269,
     DO = 270,
     END = 271,
     AND = 272,
     OR = 273,
     PLUS = 274,
     MINUS = 275,
     MULTIPLY = 276,
     DIVISION = 277,
     MODULO = 278,
     EQUAL = 279,
     LESS_THAN = 280,
     LESS_OR_EQUAL_THAN = 281,
     GREATER_THAN = 282,
     GREATER_OR_EQUAL_THAN = 283,
     DOUBLE_EQUAL = 284,
     NOT_EQUAL = 285,
     SHIFT_LEFT = 286,
     SHIFT_RIGHT = 287,
     LEFT_ROUND_PARENTHESIS = 288,
     RIGHT_ROUND_PARENTHESIS = 289,
     DOT = 290,
     COMMA = 291,
     COLON = 292,
     LEFT_CURLY_BRACE = 293,
     RIGHT_CURLY_BRACE = 294,
     LEFT_SQUARE_BRACKET = 295,
     RIGHT_SQUARE_BRACKET = 296,
     ID = 297
   };
#endif
/* Tokens.  */
#define INT 258
#define CONST 259
#define STR 260
#define LIST 261
#define OF 262
#define IF 263
#define THEN 264
#define ELSE 265
#define WHILE 266
#define FOR 267
#define IN 268
#define NOT 269
#define DO 270
#define END 271
#define AND 272
#define OR 273
#define PLUS 274
#define MINUS 275
#define MULTIPLY 276
#define DIVISION 277
#define MODULO 278
#define EQUAL 279
#define LESS_THAN 280
#define LESS_OR_EQUAL_THAN 281
#define GREATER_THAN 282
#define GREATER_OR_EQUAL_THAN 283
#define DOUBLE_EQUAL 284
#define NOT_EQUAL 285
#define SHIFT_LEFT 286
#define SHIFT_RIGHT 287
#define LEFT_ROUND_PARENTHESIS 288
#define RIGHT_ROUND_PARENTHESIS 289
#define DOT 290
#define COMMA 291
#define COLON 292
#define LEFT_CURLY_BRACE 293
#define RIGHT_CURLY_BRACE 294
#define LEFT_SQUARE_BRACKET 295
#define RIGHT_SQUARE_BRACKET 296
#define ID 297




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

