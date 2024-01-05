from faker import Faker
from typing import Dict, List

# Cria uma instância da classe Faker
fake = Faker()

tipo_dados_mapper = {
    "primeiroNome": fake.first_name,
    "sobreNome": fake.last_name,
    "nomeCompleto": fake.name,
    "nomeUser": fake.user_name,
    "prefixo": fake.prefix,
    "suffix": fake.suffix,
    "endereco": fake.address,
    "cidade": fake.city,
    "estado": fake.state,
    "pais": fake.country,
    "codigoPostal": fake.zipcode,
    "enderecoRua": fake.street_address,
    "latitude": fake.latitude,
    "longitude": fake.longitude,
    "numeroTelefone": fake.phone_number,
    "email": fake.email,
    "emailSeguro": fake.safe_email,
    "dataNasc": fake.date_of_birth,
    "dataSec": fake.date_this_century,
    "dataDec": fake.date_this_decade,
    "horario": fake.time,
    "dataHora": fake.date_time,
    "horaISO": fake.iso8601,
    "frase": fake.sentence,
    "paragrafo": fake.paragraph,
    "texto": fake.text,
    "empresa": fake.company,
    "cargo": fake.job,
    "segurancaSocial": fake.ssn,
    "numeroInteiro": fake.random_int,
    "elemento": fake.random_element,
    "amostra": fake.random_sample,
    "numeroFlutuante": fake.pyfloat,
    "url": fake.url,
    "ipv4": fake.ipv4,
    "ipv6": fake.ipv6,
    "numeroCartao": fake.credit_card_number,
    "cartaoVencimento": fake.credit_card_expire,
}

def fakeJson(json_data: Dict[str, str]) -> Dict[str, str]:
    # Itera sobre as chaves e valores do dicionário de dados
    for key, value in json_data.items():
        # Verifica se o tipo de dado é suportado
        if value in tipo_dados_mapper:
            # Substitui o valor no dicionário pelo valor gerado pela função Faker correspondente
            json_data[key] = tipo_dados_mapper[value]()
        # Levanta uma exceção se o tipo de dado não for suportado    
        else:
            raise ValueError(f"Tipo de dado não suportado para a chave '{key}': {value}")
    
    return json_data


def fakeJsonTeste(json_data: Dict[str, str]) -> Dict[str, str]:
    # Cria uma cópia do dicionário original para evitar alterações indesejadas
    result_data = json_data.copy()

    # Itera sobre as chaves e valores do dicionário de dados
    for key, value in json_data.items():
        # Verifica se o tipo de dado é suportado
        if key in tipo_dados_mapper:
            # Substitui o valor no dicionário pelo valor gerado pela função Faker correspondente
            result_data[key] = tipo_dados_mapper[key]()
        # Levanta uma exceção se a chave não for suportada    
        else:
            raise ValueError(f"Chave não suportada: {key}")

    return result_data

