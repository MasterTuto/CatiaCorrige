//100%
Algoritmo "semnome"
// Disciplina  :  [Linguagem e Lógica de Programação]
// Professor   : Antonio Carlos Nicolodi
// Descrição   : Aqui você descreve o que o programa faz! (função)
// Autor(a)    : Nome do(a) aluno(a)
// Data atual  : 24/09/2019
Var
   // Seção de Declarações das variáveis
   x: inteiro
   nota, maior, total, media: real

Inicio
   // Seção de Comandos, procedimento, funções, operadores, etc...
   maior <- 0
   para x de 1 ate 40 faca
      escreva("Escreva a nota do aluno nº ", x, ": ")
      leia(nota)

      se (nota > maior) entao
         maior <- nota
      fimse

      total <- total + nota
   fimpara

   media <- total/40

   escreval("A maior nota foi ", maior, ".")
   escreval("A média das notas é de ", media)

Fimalgoritmo