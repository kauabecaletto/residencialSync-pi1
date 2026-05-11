def ondeEsta (nom,cadastrados):
    inicio=0
    final =len(cadastrados)-1
    
    while inicio<=final:
        meio=(inicio+final)//2
        
        if nom.upper()==cadastrados[meio][0].upper():
            return [True,meio]
        elif nom.upper()<cadastrados[meio][0].upper():
            final=meio-1
        else: # nom.upper()>cadastrados[meio][0].upper()
            inicio=meio+1
            
    return [False,inicio]
   
   
   

   
   
   
    
def cadastrar(cadastrados):
    
    
        chave_para_digitar_ate_acertar_ligada=True
        while chave_para_digitar_ate_acertar_ligada:
            nome=input('Nome: ')
            senha=input('Senha: ')
        
            resposta=ondeEsta(nome,cadastrados)
            achou   = resposta[0]
            posicao = resposta[1]
        
            if achou:
                print ('Pessoa já cadastrada; tente novamente!')
            else:
             chave_para_digitar_ate_acertar_ligada=False
             contato=[nome,senha]
             cadastrados.insert(posicao,contato)
             print('Cadastro realizado com sucesso!')
             
             
#resolver o problema quando o nome nao existir
def login(cadastrados):
    nome_tentativa=input("Digite seu nome cadastrado: ")
    senha_tentativa=input("Digite sua senha cadastrada: ")
    posicao=0
    
    while len(cadastrados)>posicao:
        
        if cadastrados[posicao][0]!= nome_tentativa:
            posicao+=1
        else:
            break
        
    if posicao==len(cadastrados):
        print("usuario inexistente")
        return

    if cadastrados[posicao][1]!= senha_tentativa:
        print("alguma credencial errada")
            
    else:
        print('login efetuado')
         
            
            
           
    #um imput que vai para a tentativa_D_login e validada para ver a existecia dela
    #nos cadastrados
    
cadastrados = [] 
chave_para_Menu=True
while chave_para_Menu:
        print("""
        ╔════════════════════════════╗
        ║     SISTEMA DE ACESSO      ║
        ╠════════════════════════════╣
        ║  [1] Cadastrar             ║
        ║  [2] Login                 ║
        ║  [0] Sair                  ║
        ╚════════════════════════════╝
        """)
        
        menu_resposta = int(input("Digite a opção desejada: "))
        if menu_resposta == 1:
            cadastrar(cadastrados)
        
        elif menu_resposta==2:
             login(cadastrados)
        
        elif menu_resposta==0:
            
             chave_para_Menu=False
             print("programa encerrado")
        else:
             print("resposta invalida")
            