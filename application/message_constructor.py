# Tipos da mensagem:
# número 1 -> REQUEST
# número 2 -> GRANT
# número 3 -> OPERATION
# número 4 -> RELEASE
# número 5 -> CONNECTED

F = 27 # tamanho fixo do tamanho da mensagem
SEPARATOR = '|' # separador

# primeiro parâmetro -> identificador do tipo da messagem
# segundo parâmetro -> identificador do processo da mensagem (único para cada mensagem)
# terceiro parâmetro -> número da conta de origem da transação ou número da agência do usuário
# quarto parâmetro -> número da conta de destino da transação ou número da conta do usuário
# quinto parâmetro -> valor da transação de até 8 digitos (de 0 até 99999,99)
def message(
        type_mesage_identifier,  
        process_identifier, 
        origin_transaction,
        destination_transaction,
        value_transaction
    ):

    type_message = str(type_mesage_identifier)
    origin_account = str(origin_transaction).zfill(4)
    destination_account = str(destination_transaction).zfill(4)
    transaction_value = str(value_transaction).zfill(8)

    message = (
        type_message + # 1
        SEPARATOR + # 1
        process_identifier + # 6
        SEPARATOR + # 1
        origin_account + # 4
        SEPARATOR + # 1
        destination_account + # 4
        SEPARATOR + # 1
        transaction_value # 8
    ).zfill(F)

    if len(message) > F:
        return ("Tamanho máximo da mensagem excedido.")

    return (message)[:F]