import csv
from io import StringIO
from typing import Any, Dict, Optional, List

from mindbox.services.base import BaseMindboxAPIService
from mindbox.types.operations import RegistrationResponse


class MindboxOperationsService(BaseMindboxAPIService):
    def __init__(
        self,
        endpoint_id: str,
        secret_key: Optional[str] = None,
        device_uuid: Optional[str] = None,
        type_: str = "sync",
    ) -> None:
        """
        Initializes a new instance of the class.

        Args:
            secret_key (str): The secret key used for authentication.
            type_ (str, optional): The type of the operation (sync or async). Defaults to 'sync'.

        Returns:
            None
        """

        super().__init__(endpoint_id, secret_key, device_uuid, type_)
        self.uri = f"operations/{type_}"

    def register_client(self, operation: str, **payload) -> RegistrationResponse:
        return RegistrationResponse(**self.request("POST", self.uri, operation=operation, payload=payload))

    def update_client(self, operation: str, **payload) -> None:
        return self.request("POST", self.uri, operation=operation, payload=payload)

    def get_client(self, operation: str, **payload) -> Dict[str, Any]:
        return self.request("POST", self.uri, operation=operation, payload=payload)

    def bulk_import_client(
        self,
        operation: str,
        clients: List[Dict[str, Any]],
        csv_code_page: str = "65001",
        csv_column_delimiter: str = ";",
        csv_text_qualifier: str = '"',
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Параметры запроса

        - csvCodePage - идентификатор кодовой страницы Windows для CSV-файла.
          Предпочтительно использовать 65001 (UTF-8).
        - csvColumnDelimiter - символ, использующийся для разделения колонок в CSV-файле.
        - csvTextQualifier - символ, опционально добавляющийся в начале и в конце значения колонки,
          позволяя использовать в нём символы, обычно не разрешённые.
        - endpointId - точка доступа, из которой будут взяты настройки интеграции. Значение настраивается в системе.
        - segment - cистемное имя сегмента
        - SourceActionTemplate - действие регистрации клиента. Например, "Регистрация на сайте" или "Заполнение бумажной
          анкеты в магазине". Значение настраивается в системе.
        - editActionTemplate - действие редактирования клиента. Например, "Редактирование на сайте".
        - transactionId - ключ идемпотентности, позволяющий избежать повторного выполнения запроса.
          Ключ идемпотентности обязательно создавать в формате GUID (рекомендуется версия 4).
          Для повторных запросов c повторяющимся ключом в ответ вернется статус TransactionAlreadyProcessed.
        - данный сервис разрешает поставить не более 60 импортов в час. После превышения порога вы будете получать
          429 Too Many Requests до тех пор, пока количество поставленных задач за час не опустится ниже 60.
        - максимальный размер принимаемого файла 200мб. В случае, если необходимо загрузить больший объем данных,
          данные нужно разбить на несколько файлов.
        - поддерживается формат gzip. Для этого веб-сервер должен вернуть заголовок Content-Encoding: gzip.
          При этом файл нужно прикрепить в бинарном виде (например, binary в postman)
        """

        base_params = {
            "csvCodePage": csv_code_page,
            "csvColumnDelimiter": csv_column_delimiter,
            "csvTextQualifier": csv_text_qualifier,
        }

        if params:
            base_params.update(params)

        keys = clients[0].keys()

        f = StringIO()
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(clients)

        return self.request(
            "POST",
            self.uri,
            operation=operation,
            params=base_params,
            headers={
                "Accept": "application/json",
                "Content-Type": "text/csv;charset=utf-8",
            },
            data=f.getvalue(),
        )
