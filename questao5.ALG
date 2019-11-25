//100%
Algoritmo "semnome"
// Disciplina  :  [Linguagem e Lógica de Programação] 
// Professor   : Antonio Carlos Nicolodi 
// Descrição   : Aqui você descreve o que o programa faz! (função)
// Autor(a)    : Nome do(a) aluno(a)
// Data atual  : 24/09/2019
Var
// Seção de Declarações das variáveis
x, y, z: inteiro

Inicio
// Seção de Comandos, procedimento, funções, operadores, etc... 
para x de 1 ate 7 faca
   para z de 1 ate x faca
      escreva("*")
   fimpara

   para y de 1 ate 13-(x*2) faca
      escreva(" ")
   fimpara

   se (x = 7) entao
      x <- 6
   fimse
   para z de 1 ate x faca
      escreva("*")
   fimpara
   escreval("")
fimpara

Fimalgoritmo