import pandas as pd

# Abrindo Database
conjuntos = pd.read_csv("IA/Conjuntos.csv")
produtos = pd.read_csv("IA/Produtos.csv")
df_conjuntos = pd.DataFrame(conjuntos)
df_produtos = pd.DataFrame(produtos)

# Excluindo colunas desnecessárias

columns = ["TIPO", "COR", "CATEGORIA"]
for c in columns:
    del df_produtos[c]

conjuntos["CONJUNTO"] = conjuntos["CONJUNTO"].astype(str)

conjuntos['CONJUNTO'] = conjuntos['CONJUNTO'].apply(lambda x: [int(numero) for numero in x.split(",")])

#conjuntos["CONJUNTO"] = list(map(int, conjuntos["CONJUNTO"].split(",")))
# Definindo uma função de similaridade

def busca(search_nums, conjuntos):
    #print(search_nums)
    if len(search_nums) == 0:
        return 0
    else:
        conjuntos["bool"] = conjuntos['CONJUNTO'].apply(lambda conjunto: set(search_nums).issubset(set(conjunto)))
        #print(con)
        if True not in conjuntos["bool"].values:
            #print("Não está")
            search_nums.pop()
            busca(search_nums, conjuntos)
        else:
            return conjuntos

def drop_false(df_dropped):
    return df_dropped.drop(df_dropped[df_dropped['bool'] == False].index)
    
def similarity(search_nums, conjuntos):
    busca(search_nums, conjuntos)
    df = conjuntos
    df = drop_false(df)
    return df

def pricing(result_ids):
    total = 0
    for id in result_ids:
        total += float((df_produtos.loc[df_produtos["ID"] == id, "PRECO"].iloc[0]).replace(",", "."))
    return total

# Reusando caso e adaptando
def reuse(df, search_nums):
    if df["CONJUNTO"].values[0] == search_nums:
        print("é perfeito - ", search_nums)
    else:
        most_similar = df["CONJUNTO"].values[0]

        num_dif_remove = set(most_similar) - set(search_nums)
        num_dif_add = set(search_nums) - set(most_similar)
        
        result = set(most_similar) - set(num_dif_remove)
        result.add(*num_dif_add)
        new_price = pricing(result)
        
        # criar novo caso (objeto) com novos ids de produto e novo preço
        return {ID: "5", CONJUNTO: result, PRECO: new_price}

       
def is_clothing_type_repeated():
    # conferir se alguma peça de roupa é de tipo repetido
    # exemplo: dois tênis, duas camisas, etc

# Definindo uma função de revisão
def review():
    if not is_clothing_type_repeated():
        # adicionar à base de casos
    else:
        # remover roupas repetidas ate só ter 1 peça de cada tipo
        # aí vai cair em cima

# Teste

numeros_pesquisa = [2,19,24,8] # Array de números que deseja pesquisar
copia_numeros = []+numeros_pesquisa
df_sim = similarity(copia_numeros, conjuntos)

reuse(df_sim, numeros_pesquisa)

#similarity(animes, 50, "Action")
