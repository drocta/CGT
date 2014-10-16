CGT
===

Combinatorial Game Theory stuff.

This file provides a variety of tools for combinatorial game theory.

Features include:
going from finite integer to the corresponding surreal number game
going from non-negative integer to the corresponding nimber game
adding games, negating games, multiplying game forms
simplifying games
determining the birthday of games
determing the smallest non-negative integer greater or equal to a game
an initial attempt at creating an optimization for certain well understood games with the ga class (name potentially not final)

And an interactive calculator function called cgtshell

CGTSHELL
===
How to use cgtshell:
To use cgtshell, call cgtshell()
then enter expressions to see the outputs.
syntax for various expressions:
cgtshell for the most part uses polish notation/prefix notation, so
to add the games 2 and 2, one would say
+ 2 2
or
+ 2,2
or
+,2 2
and would recieve the answer four.
functions recognized by cgtshell are
+:addition (takes 2 arguments)
-:negation
X:multiplication (takes 2 arguments)
ceil:ceiling
eq:check for equality (output 1 for true, 0 for false) (takes 2 arguments)
sign:sign
f:modifies a game so that either player can skip a turn so long as the other player did not just skip a turn

_ represents the result of the previous expression.

To express a game,
  if the game is a finite integer, use that integer (e.g. 5. -5 would be -5 because - negates the 5. --5==5)
  if the game is a finite number, use an asterisk followed by that integer (e.g. *4 )
    * also works in place of *1
  if the game is up or down, use up or down
  to express a game in terms of its left or right options,  
    start with an open curly bracket, list the left options, use a pipe, list the right options, use a close curly bracket
    e.g. {2,*|1,*2} or {up *|down} (spaces and commas are interchangeable)

Note that games become too large to handle quickly fairly quickly.

Contribute?
===
would you like to contribute? Feel free to send a pull request for an issue, or submit an issue yourself!
