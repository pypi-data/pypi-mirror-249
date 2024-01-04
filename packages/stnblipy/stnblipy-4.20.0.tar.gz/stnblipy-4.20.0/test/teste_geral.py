import sys
sys.path.append('..')

from blipy.conexao_bd import ConexaoBD
from blipy.job import Job, TpEstrategia
from blipy.enum_tipo_col_bd import TpColBD as tp
import blipy.func_transformacao as ft


# def filtra_numero_not_null(registro):
#     # return True
#     # VALOR_ACUMULADO diferente de null
#     if registro[0] is not None:
#         return True

#     return False

# def atualiza_indices(conn_stg):
#     job = Job("Carga Indice Calculados")

#     # Carga na tabela Valor Indexador 
# # TODO: ajeitar and ((0 = 1)) no select abaixo (no talend é um parâmetro "calcula todos os anos", que fica no contexto)
# # TODO: lista de códigos em IDX.CO_BCB IN(433,189,196) é mesmo fixa ou foi só pra testes?
#     sql_entrada = """
#         select 
#                 DEV_CORPORATIVO.PKG_INDEXADORES.INDEXADOR_NO_ANO(
#                     IDX.CO_BCB,
#                     EXTRACT(year FROM VI.DT_INDEXADOR),
#                     EXTRACT(MONTH FROM VI.DT_INDEXADOR)) 
#             AS VALOR_ACUMULADO,
#             VI.ID_INDEXADOR,
#             VI.DT_INDEXADOR,
#             VI.TESTE_STRING
#         from 
#             VALOR_INDEXADOR VI, INDEXADOR IDX
#         where 
#             VI.ID_INDEXADOR = IDX.ID_INDEXADOR 
#             and IDX.CO_BCB IN (433,189,196) 
#             and (
#                 (0 = 1) 
#                 or (VI.DT_INDEXADOR = ( select 
#                                             max(VI_DENTRO.DT_INDEXADOR) 
#                                         from 
#                                             VALOR_INDEXADOR VI_DENTRO 
#                                         where 
#                                             VI.ID_INDEXADOR = VI_DENTRO.ID_INDEXADOR))
#             ) 
#         order by 
#             VI.ID_INDEXADOR, VI.DT_INDEXADOR
#         """

#     cols_saida = [ 
#         ["VA_INDEXADOR", tp.NUMBER],
#         ["ID_INDEXADOR", tp.NUMBER, ft.LookupViaTabela(
#             conn_stg, 
#             "INDEXADOR", 
#             "ID_INDEXADOR", 
#             "ID_INDEXADOR_PAI",
#             filtro="NO_FONTE = 'Calculado STN'")],  
#         ["DT_INDEXADOR", tp.DATE],
#         ["TESTE_STRING", tp.STRING]    
#     ]

#     job.importa_tabela_por_nome(
#             conn_stg, 
#             conn_stg, 
#             "VALOR_INDEXADOR_TESTE",
#             "VALOR_INDEXADOR_TESTE",
#             [
#                 "VA_INDEXADOR",
#                 "ID_INDEXADOR",
#                 "DT_INDEXADOR",
#                 "TESTE_STRING"
#             ],
#             cols_saida,
#             filtro_entrada="ID_INDEXADOR = 65",
#             estrategia=TpEstrategia.UPDATE_INSERT,
#             cols_chave_update=["ID_INDEXADOR"]
#     ) 

    # job.set_func_pre_processamento(filtra_numero_not_null)
    # job.importa_tabela_por_sql(   
    #         conn_stg, 
    #         conn_stg, 
    #         sql_entrada,
    #         "VALOR_INDEXADOR_TESTE",
    #         cols_saida,
    #         # estrategia=TpEstrategia.UPDATE_INSERT,
    #         estrategia=TpEstrategia.INSERT_UPDATE,
    #         cols_chave_update=["ID_INDEXADOR", "VA_INDEXADOR"]
    #         # cols_chave_update=["ID_INDEXADOR"]
    # ) 
    
# if __name__ == "__main__":
#     try:
#         conn_stg,  = ConexaoBD.from_json()

#         atualiza_indices(conn_stg)

# # TODO: testar carga de registros com insert e delete, pra ver se continuam funcionando
# # TODO: testar carga de registros com insert de várias linhas de uma só vez, ao mesmo tempo em que faz update linha a linha; acho que vai funcionar, pois as linhas a serem inseridas vão ficando na memória como já era antes mesmo, independentemente de algumas linhas terem sido atualizadas antes


#     except:
#         raise
#         #sys.exit(1)

# if __name__ == "__main__":
#     try:
#         conn_stg_tg, conn_dev_custos_cc = ConexaoBD.from_json([3, 1])
#         pass
#     except:
#         raise



# def atualiza_dimensao_ug_tbl(conn_stg, conn_prd):
#     job = Job("Carga de ug_tbl")

#     # dimensão UG
#     cols_entrada = [
#         "ID_UG", 
#         "TE_EXERCICIO", 
#         "NO_UG", 
#         "DT_ATUALIZACAO_CARGA", 
#         "IN_OPERACAO", 
#         "ID_UG_POLO", 
#         "ID_UG_SETORIAL_CONTABIL", 
#         "ID_ORGAO",
#         ["ID_ORGAO", "TE_EXERCICIO"]
#     ]
#     cols_saida = [  
#         ["ID_UG", tp.STRING],
#         ["TE_EXERCICIO", tp.STRING],
#         ["NO_UG", tp.STRING],
#         ["DT_ATUALIZACAO_CARGA", tp.DATE],
#         ["IN_OPERACAO", tp.STRING],
#         ["ID_UG_POLO", tp.STRING],
#         ["ID_UG_SETORIAL_CONTABIL", tp.STRING],
#         ["ID_ORGAO", tp.STRING],
#         ["NO_ORGAO", tp.STRING,
#             ft.LookupViaTabela(
#                 conn_stg, 
#                 "ORGAO", 
#                 "NO_ORGAO", 
#                 ["ID_ORGAO", "TE_EXERCICIO"])]
#     ]
#     job.importa_tabela_por_nome(
#             conn_stg, 
#             conn_prd, 
#             "UG", 
#             "UG_TBL",
#             cols_entrada, 
#             cols_saida)


# def atualiza_dimensao_servico_tbl(conn_stg, conn_prd):
#     job = Job("Carga de servico_tbl")

#     # dimensão SERVICO
#     cols_entrada = [
#         "ID_SERVICO_SK",
#         "NO_SERVICO",
#         "ID_UG",
#         "TE_EXERCICIO_UG",
#         "ID_RECOLHIMENTO_STN",
#         "TE_EXERCICIO_RECOLHIMENTO_STN",
#         "CO_TIPO_SERVICO",
#         "IN_SITUACAO",
#         "CO_CPF_USUARIO_CRIACAO",
#         "DT_CRIACAO",
#         "CO_CPF_USUARIO_ATUALIZACAO",
#         "DT_ATUALIZACAO",
#         "TX_MOTIVO_ATUALIZACAO",
#         "CO_TIPO_SERVICO"
#     ]
#     cols_saida = [  
#         ["ID_SERVICO_SK", tp.NUMBER],
#         ["NO_SERVICO", tp.STRING],
#         ["ID_UG", tp.STRING],
#         ["TE_EXERCICIO_UG", tp.STRING],
#         ["ID_RECOLHIMENTO_STN", tp.STRING],
#         ["TE_EXERCICIO_RECOLHIMENTO_STN", tp.STRING],
#         ["CO_TIPO_SERVICO", tp.STRING],
#         ["IN_SITUACAO", tp.STRING],
#         ["CO_CPF_USUARIO_CRIACAO", tp.STRING],
#         ["DT_CRIACAO", tp.DATE],
#         ["CO_CPF_USUARIO_ATUALIZACAO", tp.STRING],
#         ["DT_ATUALIZACAO", tp.DATE],
#         ["TX_MOTIVO_ATUALIZACAO", tp.STRING],
#         ["NO_TIPO_SERVICO", tp.STRING, 
#             ft.LookupViaTabela(
#                 conn_stg, 
#                 "TIPO_SERVICO", 
#                 "NO_TIPO_SERVICO", 
#                 "CO_TIPO_SERVICO")],
#     ]
#     job.importa_tabela_por_nome(
#             conn_stg, 
#             conn_prd, 
#             "SERVICO", 
#             "SERVICO_TBL",
#             cols_entrada, 
#             cols_saida)


# if __name__ == "__main__":
#     try:
#         master_job = Job("Teste Geral")

#         conn_stg, conn_prd = ConexaoBD.from_json()
    
#         atualiza_dimensao_ug_tbl(conn_stg, conn_prd)

#         atualiza_dimensao_servico_tbl(conn_stg, conn_prd)
    
#         # atualiza_fatos(conn_stg, conn_prd)

#         # master_job.grava_log_atualizacao(conn_prd)
#     except:
#         # raise
#         sys.exit(1)




if __name__ == "__main__":
    try:
        job = Job("Teste Geral")

        conn_stg, = ConexaoBD.from_json()

        job.copia_tabelas(
            conn_stg,
            conn_stg,
            [
                # ["ASSUNTO",  "NO_ASSUNTO", "ID_ASSUNTO", "ID_ASSUNTO_PAI"], 
                # ["ASSUNTO",  "NO_ASSUNTO", "ID_ASSUNTO"], 
                 # "ABRANGENCIA"
                 # "ASSUNTO",
                 # ["ABRANGENCIA", "NO_ABRANGENCIA", "SN_ATIVO", "ID_ABRANGENCIA", "QT_PONTOS"]
                 "FERRAMENTA",
                 "CADEIA_VALOR"
            ],
            # prefixo_tabelas_entrada="MVW_"
            prefixo_tabelas_saida="AA_"
        )
    
    except:
        raise

