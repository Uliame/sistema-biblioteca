import sys
import json

class Aluno:
    def __init__(self, IDAluno, nomeAluno, temLivro=False):
        self.IDAluno = IDAluno
        self.nomeAluno = nomeAluno
        self.temLivro = temLivro
        self.livrosEmprestados = [] 

    def to_dict(self):
        return {
            "IDAluno": self.IDAluno,
            "nomeAluno": self.nomeAluno,
            "temLivro": self.temLivro,
            "livrosEmprestados": self.livrosEmprestados,  
        }

    @classmethod
    def from_dict(cls, data):
        aluno = cls(data["IDAluno"], data["nomeAluno"], data["temLivro"])
        aluno.livrosEmprestados = data.get("livrosEmprestados", [])  
        return aluno

    @staticmethod
    def salvarAlunos(listaAlunos, arquivo="alunos.json"):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump([aluno.to_dict() for aluno in listaAlunos], f, ensure_ascii=False, indent=4)

    @staticmethod
    def carregarAlunos(arquivo="alunos.json"):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                alunos_dict = json.load(f)
                return [Aluno.from_dict(aluno) for aluno in alunos_dict]
        except FileNotFoundError:
            return []

    def pegarEmprestado(self, livro):
        if livro.titulo not in self.livrosEmprestados:
            self.livrosEmprestados.append(livro.titulo)
            self.temLivro = True 
        else:
            print(f"{self.nomeAluno} já pegou o livro {livro.titulo}.")

    def devolver(self, livro):
        if livro.titulo in self.livrosEmprestados:
            self.livrosEmprestados.remove(livro.titulo) 
            if not self.livrosEmprestados:
                self.temLivro = False 
        else:
            print(f"{self.nomeAluno} não pegou o livro {livro.titulo}.")

class Livro:
    def __init__(self, IDLivro, ISBN, titulo, autor, quantidade):
        self.IDLivro = IDLivro
        self.ISBN = ISBN
        self.titulo = titulo
        self.autor = autor
        self.quantidade = int(quantidade)
        self.qtdEmprest = 0

    def to_dict(self):
        return {"IDLivro": self.IDLivro, "ISBN": self.ISBN, "titulo": self.titulo, "autor": self.autor, "quantidade": self.quantidade, "qtdEmprest": self.qtdEmprest}

    @classmethod
    def from_dict(cls, data):
        livro = cls(data["IDLivro"], data["ISBN"], data["titulo"], data["autor"], data["quantidade"])
        livro.qtdEmprest = data.get("qtdEmprest", 0) 
        return livro

    def emprestimo(self):
        if self.qtdEmprest < self.quantidade:
            self.qtdEmprest += 1
        else:
            print("Não ha mais copias disponiveis deste livro.")

    def devolucao(self):
        if self.qtdEmprest > 0:
            self.qtdEmprest -= 1
        else:
            print("Nenhum livro foi emprestado.")

class Biblioteca:
    def __init__(self):
        self.livros = []
        self.carregarLivros()

    def adicionarLivro(self, livro):
        self.livros.append(livro)
        self.salvarLivros()

    def salvarLivros(self):
        with open("livros.json", "w", encoding="utf-8") as f:
            livros_dict = [livro.to_dict() for livro in self.livros]  
            json.dump(livros_dict, f, ensure_ascii=False, indent=4)

    def carregarLivros(self):
        try:
            with open("livros.json", "r", encoding="utf-8") as f:
                livros_dict = json.load(f)
                self.livros = [Livro.from_dict(livro) for livro in livros_dict]  
        except FileNotFoundError:
            pass  

    def listarLivros(self):
        if self.livros:
            print("\n------------CATALOGO DE LIVROS------------")
            for livro in self.livros:
                print(f"ID: {livro.IDLivro}")
                print(f"ISBN: {livro.ISBN}")
                print(f"Titulo: {livro.titulo}")
                print(f"Autor: {livro.autor}")
                print(f"Copias: {livro.quantidade} Emprestados: {livro.qtdEmprest}")
                print("-\n")
        else:
            print("\nNenhum livro no catalogo.\n")

def cadastrarAluno():
    print("\n------------CADASTRO DE ALUNO------------\n")
    IDAluno = input("Digite o ID do aluno: ")
    nome = input("Digite o nome do aluno: ")

    aluno = Aluno(IDAluno, nome)
    return aluno

def cadastrarLivro():
    print("\n------------CADASTRO DE LIVRO------------\n")
    IDLivro = input("Digite o ID do Livro: ")
    ISBN = input("Digite o ISBN do livro: ")
    titulo = input("Digite o titulo do livro: ")
    autor = input("Digite o autor do livro: ")
    quantidade = input("Digite quantas copias existem: ")

    livro = Livro(IDLivro, ISBN, titulo, autor, quantidade)
    return livro

def listarAlunos(listaAlunos):
    if listaAlunos:
        print("\n------------ALUNOS CADASTRADOS------------")
        for aluno in listaAlunos:
            status = "TEM LIVROS EMPRESTADOS" if aluno.temLivro else "SEM EMPRESTIMO"
            print(f"{aluno.IDAluno}  {aluno.nomeAluno} - {status}")
    else:
        print("Nenhum aluno cadastrado.\n")

def emprestarLivros():
    print("\n------------EMPRESTIMO------------")

    listarAlunos(listaAlunos)
    IDAluno = input("Digite o ID do aluno: ")

    alunoEncontrado = next((a for a in listaAlunos if a.IDAluno == IDAluno), None)
    if not alunoEncontrado:
        print("Aluno nao encontrado.")
        return

    qtdLivros = int(input("Quantos livros deseja pegar emprestado? "))
    biblioteca.listarLivros()
    for _ in range(qtdLivros):
        IDLivro = input("Digite o ID do livro: ")
        livroEncontrado = next((l for l in biblioteca.livros if l.IDLivro == IDLivro), None)
        if not livroEncontrado:
            print("Livro nao encontrado.")
            continue
        if livroEncontrado.qtdEmprest >= livroEncontrado.quantidade:
            print(f"{livroEncontrado.titulo} nao disponivel para emprestimo.")
            continue
        alunoEncontrado.pegarEmprestado(livroEncontrado)  
        livroEncontrado.emprestimo()  
        print(f"Livro {livroEncontrado.titulo} emprestado para {alunoEncontrado.nomeAluno}.\n")

    Aluno.salvarAlunos(listaAlunos)
    biblioteca.salvarLivros()
    print("Emprestimo finalizado!")

def devolverLivro():
    print("\n------------DEVOLUCAO------------")

    listarAlunos(listaAlunos)
    IDAluno = input("Digite o ID do aluno: ")
    alunoEncontrado = next((a for a in listaAlunos if a.IDAluno == IDAluno), None)
    if not alunoEncontrado:
        print("Aluno nao encontrado.")
        return
    if not alunoEncontrado.livrosEmprestados:
        print(f"{alunoEncontrado.nomeAluno} nao tem livros emprestados.")
        return
    
    print("\nLivros emprestados: ")
    livros_para_devolver = []  
    for livro in biblioteca.livros:
        if livro.titulo in alunoEncontrado.livrosEmprestados:
            livros_para_devolver.append(livro)
    if not livros_para_devolver:
        print("Erro: Nenhum livro correspondente foi encontrado na biblioteca.")
        return
    for livro in livros_para_devolver:
        print(f"{livro.IDLivro} - {livro.titulo}")

    qtdLivros = int(input("Quantos livros deseja devolver? "))

    for _ in range(qtdLivros):
        IDLivro = input("Digite o ID do livro: ")
        livroEncontrado = next((l for l in biblioteca.livros if l.IDLivro == IDLivro), None)

        if not livroEncontrado:
            print(f"Livro com ID {IDLivro} nao encontrado.")
            continue
        if livroEncontrado.titulo not in alunoEncontrado.livrosEmprestados:
            print(f"Este livro nao foi emprestado para {alunoEncontrado.nomeAluno}.")
            continue
        alunoEncontrado.devolver(livroEncontrado)  
        livroEncontrado.devolucao()
        print(f"{livroEncontrado.titulo} devolvido!\n")

    Aluno.salvarAlunos(listaAlunos)
    biblioteca.salvarLivros()
    print("Devolução finalizada!")


def menu():
    return int(input(
        "\n------------Menu------------\n"
        "1: Cadastrar Aluno\n"
        "2: Cadastrar Livro\n"
        "3: Emprestar Livros\n"
        "4: Devolver Livros\n"
        "5: Exibir lista de Alunos\n"
        "6: Exibir lista de Livros\n"
        "0: Encerrar Sistema\n"
    ))

biblioteca = Biblioteca()
listaAlunos = Aluno.carregarAlunos()

while True:
    choice = menu()
    if choice == 1:
        aluno = cadastrarAluno()
        listaAlunos.append(aluno)
        Aluno.salvarAlunos(listaAlunos)
    elif choice == 2:
        livro = cadastrarLivro()
        biblioteca.adicionarLivro(livro)
    elif choice == 3:
        emprestarLivros()
    elif choice == 4:
        devolverLivro()
    elif choice == 5:
        listarAlunos(listaAlunos)
        input("")
    elif choice == 6:
        biblioteca.listarLivros()
        input("")
    elif choice == 0:
        sys.exit()
    else:
        print("OPCAO INVALIDA.")