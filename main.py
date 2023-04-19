import pandas as pd
from classes.ClothingSet import ClothingSet

# Abrindo dataframe
conjuntos = pd.read_csv("dataframes/Conjuntos.csv")
produtos = pd.read_csv("dataframes/Produtos.csv")

df_conjuntos = pd.DataFrame(conjuntos)
df_produtos = pd.DataFrame(produtos)

# Excluindo colunas desnecessárias
columns = ["TIPO", "COR", "CATEGORIA"]
for c in columns:
    del df_produtos[c]

# Tratando dados da planilha
conjuntos['CONJUNTO'] = conjuntos['CONJUNTO'].str.replace('[', '')
conjuntos['CONJUNTO'] = conjuntos['CONJUNTO'].str.replace(']', '')
conjuntos['CONJUNTO'] = conjuntos['CONJUNTO'].apply(lambda x: [int(numero) for numero in x.split(",")])

# Buscando casos mais similares
def busca(search_nums, conjuntos):
    if len(search_nums) == 0:
        return 0
    else:
        conjuntos["bool"] = conjuntos['CONJUNTO'].apply(lambda conjunto: set(search_nums).issubset(set(conjunto)))
        if True not in conjuntos["bool"].values:
            search_nums.pop()
            busca(search_nums, conjuntos)
        else:
            return conjuntos

# Dropando casos não similares
def drop_false(df_dropped):
    return df_dropped.drop(df_dropped[df_dropped['bool'] == False].index)
    
# Aplicando função de similaridade
def similarity(search_nums, conjuntos):
    x = busca(search_nums, conjuntos)
    df = conjuntos
    df = drop_false(df)
    return df

# Tratando o preço
def pricing(result_ids):
    total = 0
    for id in result_ids:
        total += float((df_produtos.loc[df_produtos["ID"] == id, "PRECO"].iloc[0]).replace(",", "."))
    return total

# Reusando caso e adaptando
def reuse(df, search_nums):
    if set(df["CONJUNTO"].iloc[0]) == set(search_nums):
        return df["CONJUNTO"].iloc[0]
    else:
        most_similar = df["CONJUNTO"].iloc[0]

        num_dif_remove = set(most_similar) - set(search_nums)
        num_dif_add = set(search_nums) - set(most_similar)
        
        result = set(most_similar) - set(num_dif_remove)
        for i in [*num_dif_add]:
            result.add(i)
        result = list(result)
        new_price = pricing(result)
        
        new_case = ClothingSet(result, new_price)
        return new_case
    
# Pegando o tipo da roupa pelo id
def get_type_from_id(id):
    type = produtos.loc[produtos["ID"] == id, "VESTIR"].iloc[0]
    return [type, id]

# Adicionando função de revisão
def revise(clothes):
    types = []
    for clothing in clothes.conjunto:
        types.append(get_type_from_id(clothing))

    repeated = {}
    for item in types:
        if item[0] in repeated:
            repeated[item[0]].append(item[1])
        else:
            repeated[item[0]] = [item[1]]

    for chave, valores in repeated.items():
        if len(valores) > 1:
            print(f"O primeiro elemento '{chave}' está repetido com os segundos elementos {valores}")
            clothes.conjunto.remove(valores[0])
    return clothes        
    
# Adicionando novo caso à base
def add_new_case(case, df):
    nova_linha = pd.Series(case.toArray(), index=df.columns)
    df.loc[-1] = nova_linha
    df = df.reset_index(drop=True)
    df.to_csv('dataframes/Conjuntos.csv', index=False)

# Teste
numeros_pesquisa = [4,21,24,7] # Array de números que deseja pesquisar
copia_numeros = []+numeros_pesquisa
df_sim = similarity(copia_numeros, conjuntos)
del df_sim["bool"]
case = reuse(df_sim, numeros_pesquisa)
new_case = revise(case)
del conjuntos["bool"]

add_new_case(new_case, conjuntos)
print(conjuntos)

