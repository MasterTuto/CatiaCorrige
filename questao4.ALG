//100%
Algoritmo "semnome"
// Disciplina  :  [Linguagem e Lógica de Programação] 
// Professor   : Antonio Carlos Nicolodi 
// Descrição   : Aqui você descreve o que o programa faz! (função)
// Autor(a)    : Nome do(a) aluno(a)
// Data atual  : 24/09/2019
Var
// Seção de Declarações das variáveis 
x, cont: inteiro

Inicio
// Seção de Comandos, procedimento, funções, operadores, etc... 
cont <- 0

para x de 1000 ate 1999 faca
   se ( x % 11=5) entao
      escreval("Achei um, eba! Ele é ", x)
      cont <- cont + 1
      se (cont=20) entao
         escreva("Achei todos...")
         interrompa
      fimse
   fimse
fimpara


Fimalgoritmo