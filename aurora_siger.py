"""
Projeto Aurora Siger
Verificador de dados de múltiplas missões

"""
# Importações para iniciar o código
import csv
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Ranges de validação
RANGES = {
    "temp_interna":  (18.0,   27.0),
    "temp_externa":  (-50.0,  60.0),
    "integridade":   (1,      1),       # necessário ser 1
    "energia":       (95.0,   100.0),
    "pressao":       (300.0,  350.0),
    "modulos":       (1,      1),       # necessário ser 1
}

# Tradução dos itens
LABELS = {
    "temp_interna": "Temperatura interna (°C)",
    "temp_externa": "Temperatura externa (°C)",
    "integridade":  "Integridade estrutural (1=OK)",
    "energia":      "Nível de energia (%)",
    "pressao":      "Pressão dos tanques (psi)",
    "modulos":      "Módulos críticos (1=OK)",
}

# Criação do SET com uso de unpacking
COLUNAS_OBRIGATORIAS = {"missao", *RANGES.keys()}


# Estrutura
@dataclass
class ResultadoMissao:
    missao: str
    aprovada: bool
    falhas: list = field(default_factory=list)
    valores: dict = field(default_factory=dict)

# Validação da missão
def validar_missao(row: dict) -> ResultadoMissao:
    falhas = []
    valores = {}

    for campo, (minimo, maximo) in RANGES.items():
        raw = row.get(campo, "").strip()
        try:
            valor = int(raw) if campo in ("integridade", "modulos") else float(raw)
        except ValueError:
            falhas.append(f"{LABELS[campo]}: valor inválido '{raw}'")
            valores[campo] = raw
            continue

        valores[campo] = valor
        if not (minimo <= valor <= maximo):
            if minimo == maximo:
                falhas.append(f"{LABELS[campo]}: esperado {int(minimo)}, recebido {valor}")
            else:
                falhas.append(f"{LABELS[campo]}: {valor} fora de [{minimo} – {maximo}]")

    return ResultadoMissao(
        missao=row.get("missao", "?"),
        aprovada=len(falhas) == 0,
        falhas=falhas,
        valores=valores,
    )

# Leitura do CSV
def carregar_csv(caminho: Path) -> list: # Definição do local onde o .CSV se encontra para ser importado
    if not caminho.exists():
        sys.exit(f"Erro: arquivo '{caminho}' não encontrado.") # Mensagem de erro caso não encontre o arquivo

    with caminho.open(newline="", encoding="utf-8") as f: # Newline para evitar leitura errada do arquivo
        reader = csv.DictReader(f)
        colunas = set(reader.fieldnames or [])
        faltando = COLUNAS_OBRIGATORIAS - colunas
        if faltando:
            sys.exit(f"Erro: colunas ausentes no CSV: {', '.join(sorted(faltando))}") # Mensagem de erro com exit caso haja colunas ausentes no arquivo .CSV
        return list(reader) # Voltar o código para continuar a interação

# Geração do relatório
def gerar_relatorio(resultados: list, caminho_csv: Path) -> str: # Definição de local para a geração do arquivo
    total      = len(resultados)
    aprovadas  = sum(1 for r in resultados if r.aprovada)
    reprovadas = total - aprovadas
    agora      = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # Definição do formato do horário na geração do arquivo

    linhas = [
        "=" * 60, # Separador padrão de linhas para arquivos .TXT
        "   RELATÓRIO DE VERIFICAÇÃO DE DECOLAGEM",
        f"   Arquivo : {caminho_csv.name}",
        f"   Gerado  : {agora}", # Retorna o horário da geração do relatório
        "=" * 60,
        f"   Total de missões : {total}",
        f"   ✔ Aprovadas       : {aprovadas}",
        f"   ✘ Reprovadas      : {reprovadas}",
        "=" * 60,
    ]

# Contagem dos resultados
    for r in resultados:
        status = "✔ APROVADA" if r.aprovada else "✘ REPROVADA"
        linhas.append(f"\n  Missão : {r.missao}  [{status}]")
        linhas.append("  " + "-" * 40)

# Loop de interações
        for campo, label in LABELS.items():
            valor = r.valores.get(campo, "N/A") # Busca dos valores e retorno do N/A caso não encontrado
            minimo, maximo = RANGES[campo]
            try:
                ok = "✔" if minimo <= float(valor) <= maximo else "✘" # Verifica se o valor buscado acima está dentro do range
            except (ValueError, TypeError): # Retorna o X caso o campo esteja inválido
                ok = "✘"
            linhas.append(f"    {ok}  {label:<35} {valor}")

        if r.falhas: # Marcador de falhas
            linhas.append("\n     Falhas detectadas:")
            for falha in r.falhas:
                linhas.append(f"       • {falha}")

    linhas += [ # Final do relatório
        "\n" + "=" * 60,
        "   FIM DO RELATÓRIO",
        "=" * 60,
    ]

    return "\n".join(linhas) # Agrupa tudo para facilitar a impressão

# Salvar relatório em .txt
def salvar_relatorio(texto: str, caminho_csv: Path) -> Path:
    saida = caminho_csv.parent / f"relatorio_{caminho_csv.stem}.txt"
    saida.write_text(texto, encoding="utf-8")
    return saida

# Main
def main() -> None: # Não retorna nada, apenas executa
    caminho_csv = Path("dados_missao.csv")
    # Importa o arquivo "dados_missao"

    print(f"\nCarregando CSV: {caminho_csv}")
    rows = carregar_csv(caminho_csv)
    print(f"{len(rows)} missão(ões) encontrada(s). Validando...\n")

    resultados = [validar_missao(row) for row in rows] # Cria a lista de itens

    relatorio = gerar_relatorio(resultados, caminho_csv) # Salva os dados em relatorio
    print(relatorio)

    saida = salvar_relatorio(relatorio, caminho_csv) # Salva o arquivo .TXT
    print(f"\n📄 Relatório salvo em: {saida}")

if __name__ == "__main__":
    main()
