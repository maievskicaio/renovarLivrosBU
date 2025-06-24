from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


arquivo = open("login.txt", "r")
login = arquivo.read()
arquivo.close()
login = login.split(";")
listaLivros = []


# Abre o domínio de login da biblioteca.
driver = webdriver.Chrome()
driver.get("https://pergamumweb.udesc.br/login?redirect=/")

# Pesquisa o campo de USUÁRIO e insere o valor no campo.
user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
user = driver.find_element(By.NAME, "username")
user.send_keys(login[0])

# Pesquisa o campo de SENHA e insere o valor no campo.
passw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
passw = driver.find_element(By.NAME, "password")
passw.send_keys(login[1])

# Efetua o login
entrar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pergamum']/div/div[1]/div/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/button[1]")))
entrar = driver.find_element(By.XPATH, "//*[@id='pergamum']/div/div[1]/div/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/button[1]")
entrar.send_keys(Keys.ENTER)

# Renova empréstimos possiveis
titulos = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mp-root']/div/div[1]/div[5]/div/div[2]/div[2]/div/div[1]")))
titulos = driver.find_element(By.XPATH, "//*[@id='mp-root']/div/div[1]/div[5]/div/div[2]/div[2]/div/div[1]")
rows = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "row")))
rows = titulos.find_elements(By.CLASS_NAME, "row")
sleep(2)
for row in (enumerate(rows)):
    if row[0] == 0:
        continue
    livros = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "align-self-center")))
    livros = row[1].find_elements(By.CLASS_NAME, "align-self-center")
    for livro in (enumerate(livros)):
        if livro[0] == 0:
            caminho = "//*[@id='mp-root']/div/div[1]/div[5]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[{}]/div[1]".format(row[0] + 1)
            nomeLivro = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, caminho)))
            nomeLivro = livro[1].find_element(By.XPATH, caminho)
            nomeLivro = nomeLivro.find_elements(By.TAG_NAME, "span")
            nomeLivro = nomeLivro[2].text
            print(nomeLivro)
            listaLivros.append(nomeLivro)
        if livro[0] == 3:
            caminho = "//*[@id='mp-root']/div/div[1]/div[5]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[{}]/div[4]/button".format(row[0] + 1)
            click = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, caminho)))
            click = livro[1].find_element(By.XPATH, caminho)
            click.click()

# Informa quais livros foram renovados
print("LIVROS ENCONTRADOS: ")
for i in (enumerate(listaLivros)):
    print("[{}] {}".format(i[0]+1, i[1]))
sleep(10)
