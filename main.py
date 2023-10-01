import tkinter as tk
from tkinter import filedialog
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Função para abrir o arquivo DICOM e exibir a imagem
def abrir_arquivo_dicom():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos DICOM", "*.dcm")])
    
    if file_path:
        dcm_data = pydicom.dcmread(file_path)
        imagem = dcm_data.pixel_array
        
        # Exibir a imagem usando o matplotlib no Tkinter
        plt.figure(figsize=(5, 5))
        plt.imshow(imagem, cmap=plt.cm.bone)
        plt.axis('off')
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.get_tk_widget().pack()
        canvas.draw()
        
        # Atualizar a imagem exibida e o caminho do arquivo
        global imagem_exibida, arquivo_aberto
        imagem_exibida = imagem
        arquivo_aberto = file_path

# Função para salvar a imagem como PNG com o mesmo nome do arquivo DICOM
def salvar_como_png():
    if 'imagem_exibida' in globals():
        if imagem_exibida is not None:
            if 'arquivo_aberto' in globals():
                if arquivo_aberto:
                    # Obtenha o diretório e o nome do arquivo DICOM original
                    diretorio, nome_arquivo = os.path.split(arquivo_aberto)
                    
                    # Crie o nome do arquivo PNG com a mesma base de nome
                    nome_arquivo_png = os.path.splitext(nome_arquivo)[0] + ".png"
                    
                    # Combine o diretório e o novo nome do arquivo
                    caminho_destino = os.path.join(diretorio, nome_arquivo_png)
                    
                    # Salve a imagem como PNG
                    plt.imsave(caminho_destino, imagem_exibida, cmap=plt.cm.bone)
                    print(f'Imagem salva como {caminho_destino}')

# Função para converter todos os arquivos .dcm em .png no diretório atual
def converter_arquivos_dcm_em_png():
    try:
        diretorio_atual = os.getcwd()
        
        # Liste todos os arquivos no diretório atual
        arquivos = os.listdir(diretorio_atual)
        
        # Itere sobre os arquivos e converta aqueles com extensão .dcm em .png
        for arquivo in arquivos:
            if arquivo.endswith(".dcm"):
                caminho_completo = os.path.join(diretorio_atual, arquivo)
                dcm_data = pydicom.dcmread(caminho_completo)
                imagem = dcm_data.pixel_array
                nome_arquivo_png = os.path.splitext(arquivo)[0] + ".png"
                caminho_destino = os.path.join(diretorio_atual, nome_arquivo_png)
                plt.imsave(caminho_destino, imagem, cmap=plt.cm.bone)
                print(f'{arquivo} convertido para {nome_arquivo_png}')
        
        print('Conversão concluída.')
    except Exception as e:
        print(f'Ocorreu um erro ao converter os arquivos: {str(e)}')

# Função para excluir todos os arquivos .dcm no diretório atual
def excluir_arquivos_dcm():
    try:
        diretorio_atual = os.getcwd()
        # Liste todos os arquivos no diretório atual
        arquivos = os.listdir(diretorio_atual)
        
        # Itere sobre os arquivos e exclua aqueles com extensão .dcm
        for arquivo in arquivos:
            if arquivo.endswith(".dcm"):
                caminho_completo = os.path.join(diretorio_atual, arquivo)
                os.remove(caminho_completo)
                print(f'Arquivo {caminho_completo} excluído com sucesso!')
        
        print('Todos os arquivos .dcm no diretório atual foram excluídos.')
    except Exception as e:
        print(f'Ocorreu um erro ao excluir os arquivos: {str(e)}')

# Criar a janela principal
root = tk.Tk()
root.title("DICOMViewer")

# Botão para escolher o arquivo DICOM
abrir_botao = tk.Button(root, text="Abrir Arquivo DICOM", command=abrir_arquivo_dicom)
abrir_botao.pack(pady=10)

# Botão para salvar como PNG com o mesmo nome do arquivo DICOM
salvar_botao = tk.Button(root, text="Salvar como PNG", command=salvar_como_png)
salvar_botao.pack()

# Botão para converter todos os arquivos .dcm em .png no diretório atual
converter_botao = tk.Button(root, text="Converter Arquivos DICOM em PNG", command=converter_arquivos_dcm_em_png)
converter_botao.pack()

# Botão para excluir todos os arquivos .dcm no diretório atual
excluir_botao = tk.Button(root, text="Excluir Arquivos DICOM", command=excluir_arquivos_dcm)
excluir_botao.pack()

# Executar a interface gráfica
root.mainloop()

