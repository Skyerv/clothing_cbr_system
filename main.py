import pandas as pd

from classes.ClothingSet import ClothingSet

# Abrindo Database
conjuntos = pd.read_csv("dataframes/Conjuntos.csv")
produtos = pd.read_csv("dataframes/Produtos.csv")
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
        result = list(result)
        new_price = pricing(result)
        
        id = df.iloc[df.shape[0]-1]['ID']
        # criar novo caso (objeto) com novos ids de produto e novo preço
        new_case = ClothingSet(id, result, new_price)
        # print(new_case.id, new_case.conjunto, new_case.preco)
        return new_case
    
def get_type_from_id(id):
    type = produtos.loc[produtos["ID"] == id, "VESTIR"].iloc[0]

    return [type, id]

# def 

def has_repeated_types(clothes):
    # conferir se alguma peça de roupa é de tipo repetido
    # exemplo: dois tênis, duas camisas, etc
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
            print(clothes.conjunto)
    return clothes        
    
def add_new_case(case, df):
    
    nova_linha = pd.Series(case.toArray(), index=df.columns)
    df.loc[-1] = nova_linha
    df = df.reset_index(drop=True)
    df.to_csv('dataframes/Conjuntos.csv')
    #print(case)
# Definindo uma função de revisão
# def review(clothes):
#     repeated_types = has_repeated_types(clothes)
#     if repeated_types is not None:
#         print(repeated_types)
#         for i in repeated_types:
#             clothes.conjunto.remove(i)
            
#         print(clothes.conjunto)
#     else:
#         print("Não há valores repetidos")
# Teste

numeros_pesquisa = [2,19,24,8] # Array de números que deseja pesquisar
copia_numeros = []+numeros_pesquisa
df_sim = similarity(copia_numeros, conjuntos)

case = reuse(df_sim, numeros_pesquisa)
caso_mockado = ClothingSet("59", [2, 5, 10, 13], 210.20)
new_case = has_repeated_types(caso_mockado)

del conjuntos["bool"]

add_new_case(new_case, conjuntos)

#similarity(animes, 50, "Action")
