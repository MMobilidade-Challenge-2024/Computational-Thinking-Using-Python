import json
from datetime import datetime


def load_json(json_name: str = "failures.json") -> list:
    """Tenta carregar uma lista a partir de um arquivo JSON com o nome indicado. Caso não exista, cria o arquivo e
    retorna a lista vazia."""

    def create_json(name: str = "failures.json"):
        """Cria um arquivo JSON contendo uma lista vazia com o nome indicado."""
        with open(name, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    try:
        with open(json_name, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        create_json(json_name)
        return load_json(json_name)


def save_on_json(list_to_save: list, json_name: str = "failures.json"):
    """Salva uma lista no arquivo JSON indicado. Caso o arquivo não exista, ele será criado antes de salvar os dados."""
    load_json(json_name)
    with open(json_name, "w", encoding="utf-8") as file:
        json.dump(list_to_save, file, indent=4)


def create_failure():
    """Cria um registro de falha (ID, data, tipo, descrição) e o salva em um arquivo JSON."""

    def generate_failure_type() -> str:
        """Retorna um str com o tipo de falha para colocar no sistema."""
        while True:
            try:
                print("\nEscolha o tipo de falha:\n" + "=" * 50 +
                      "\n1. Mecânica\n"
                      "2. Elétrica\n"
                      "3. Software\n"
                      "4. Outro\n" +
                      "-" * 50)
                option = int(input("Digite a opção desejada:\n"))
                match option:
                    case 1:
                        return "MECANICA"
                    case 2:
                        return "ELETRICA"
                    case 3:
                        return "SOFTWARE"
                    case 4:
                        return "OUTRO"
                    case _:
                        print("Opção Inválida")
            except ValueError:
                print("Valor inválido")

    failures_list = load_json()
    falha = {
        "failure_id": len(failures_list) + 1,
        "date": datetime.today().strftime("%d/%m/%Y - %H:%M"),
        "type": generate_failure_type(),
        "description": input("Digite a descrição da falha:\n"),
        "on_report": False
    }
    failures_list.append(falha)
    save_on_json(failures_list)
    print(f"Falha #{falha['failure_id']} adicionada ao sistema.\n")


def generate_report() -> None:
    """Gera um relatório básico de falhas (ID, falha mais frequente, número total de falhas não reportadas) e o salva
    em um JSON, atualizando o status das falhas reportadas."""

    all_failures = load_json()
    failures_on_report = [failure for failure in all_failures if failure["on_report"] is True]

    failures_to_report = [failure for failure in all_failures if failure["on_report"] is False]
    if len(failures_to_report) == 0:
        print("Não há falhas para reportar.")
        return

    report_list = load_json("reports.json")
    fail_types = [failure["type"] for failure in failures_to_report]
    report = {
        "id_report": len(report_list) + 1,
        "most_frequent_failure": max(fail_types, key=fail_types.count),
        "number_of_failures": len(failures_to_report)
    }
    report_list.append(report)

    for failure in failures_to_report:
        failure["on_report"] = True

    all_failures = failures_on_report + failures_to_report

    save_on_json(all_failures)
    save_on_json(report_list, "reports.json")

    print(f"Relatório #{report['id_report']}:\n"
          f"Falha mais frequente: {report['most_frequent_failure']}\n"
          f"Número de falhas: {report['number_of_failures']}")


def start_system(adm_permission: bool = False) -> int:
    """Inicia o sistema, recebe a permissão de administrador (se aplicável) e retorna um inteiro para ser usado no
    menu de login."""

    def show_failure_history() -> None:
        """Mostra o histórico de falhas formatado."""
        history = ""

        for fail in load_json():
            fail_id = fail["failure_id"]
            fail_date = fail["date"]
            fail_type = fail["type"]
            fail_description = fail["description"]
            history += f"#{fail_id} ({fail_date}) | {fail_type} - {fail_description}\n"

        if history == "":
            history = "Não há registros"

        print(f"Dados do histórico:\n{history}")

    def show_report_history() -> None:
        """Mostra o histórico de relatórios formatado."""
        history = ""

        for report in load_json("reports.json"):
            report_id = report["id_report"]
            report_frequent_failure = report["most_frequent_failure"]
            report_num_failures = report["number_of_failures"]
            history += f"#{report_id} | {report_frequent_failure} - Número de falhas: {report_num_failures}\n"

        if history == "":
            history = "Não há registros"

        print(f"Dados do histórico:\n{history}")

    system_menu_adm = ("\nBem-vindo, Administrador!\n" + "=" * 50 +
                       "\n1. Registrar nova falha\n"
                       "2. Exibir histórico de falhas\n"
                       "3. Gerar relatório de falhas\n"
                       "4. Exibir histórico de relatórios\n"
                       "5. Voltar para os logins\n"
                       "0. Sair\n" +
                       "-" * 50)

    system_menu = ("\nBem-vindo, Operador!\n" + "=" * 50 +
                   "\n1. Registrar nova falha\n"
                   "2. Exibir histórico de falhas\n"
                   "3. Exibir histórico de relatórios\n"
                   "4. Voltar para os logins\n"
                   "0. Sair\n" +
                   "-" * 50)

    menu = system_menu_adm if adm_permission else system_menu
    if adm_permission:
        while True:
            try:
                print(menu)
                option = int(input("Digite a opção desejada:\n"))

                match option:
                    case 0:
                        return 0
                    case 1:
                        create_failure()
                    case 2:
                        show_failure_history()
                    case 3:
                        generate_report()
                    case 4:
                        show_report_history()
                    case 5:
                        return -1
                    case _:
                        print("Opção Inválida")
            except ValueError:
                print("Valor inválido")
    else:
        while True:
            try:
                print(menu)
                option = int(input("Digite a opção desejada:\n"))

                match option:
                    case 0:
                        return 0
                    case 1:
                        create_failure()
                    case 2:
                        show_failure_history()
                    case 3:
                        show_report_history()
                    case 4:
                        return -1
                    case _:
                        print("Opção Inválida")
            except ValueError:
                print("Valor inválido")


def start_login() -> None:
    """Exibe o menu de login para operadores e administradores."""
    option = -1
    login_menu = ("\nEscolha um:\n"
                  "1. Operador\n"
                  "2. Administrador\n"
                  "0. Sair\n" +
                  "-" * 50)

    print(f"Marmota Mobilidade\nBem vindo ao sistema de histórico de falhas!\n" + "=" * 50)
    while True:
        try:
            option = -1 if option != 0 else 0
            if option == 0:
                print("Saindo...")
                break

            print(login_menu)
            option = int(input("Digite a opção desejada:\n"))

            match option:
                case 0:
                    continue
                case 1:
                    print("Logando como operador...")
                    option = start_system()
                case 2:
                    print("Logando como administrador...")
                    option = start_system(True)
                case _:
                    print("Opção inválida")

        except ValueError:
            print("Valor inválido")


start_login()
