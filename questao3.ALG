//100%
Algoritmo "semnome"
// Disciplina  :  [Linguagem e Lógica de Programação]
// Professor   : Antonio Carlos Nicolodi
// Descrição   : Aqui você descreve o que o programa faz! (função)
// Autor(a)    : Nome do(a) aluno(a)
// Data atual  : 24/09/2019
Var
   // Seção de Declarações das variáveis
   opcao: inteiro
   valor: real


Inicio
   // Seção de Comandos, procedimento, funções, operadores, etc...
   escreval("ESCOLHA UMA DAS OPÇÕES: ")
   escreval("[1] Converter R$ em US$")
   escreval("[2] Converter US$ em R$")
   escreval("[3] FIM")

   escreva("Escreva a opção desejada: ")
   leia(opcao)

   enquanto (opcao <> 3) faca
      escolha opcao
      caso 1
         escreva("Insira um valor em reais: ")
         leia(valor)

         escreval("================")
         escreval("== O valor em dólares é: US$ ", valor * 0.25, " ==")
         escreval("================")

      caso 2
         escreva("Insira um valor em dólares: ")
         leia(valor)

         escreval("================")
         escreval("== O valor em reais é: R$ ", valor * 4.00, " ==")
         escreval("================")

      outrocaso
         escreval("Opção inválida, tente de novo.")
      fimescolha

      escreva("Quer continuar tentantando? Insira uma opção: ")
      leia(opcao)

   fimenquanto

   escreval("Até mais...")

Fimalgoritmo