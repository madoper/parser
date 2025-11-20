# Руководство по семантической разметке кода для ИИ-ассистентов

## 1. Введение

Данное руководство определяет стандарты семантической разметки кода для проекта парсера сайтов. Цель семантической разметки — обеспечить максимальную понятность кода для ИИ-ассистентов, что упрощает автоматическую генерацию кода, рефакторинг и анализ.

## 2. Стандарты именования компонентов

### 2.1. Общие принципы

- Используйте осмысленные имена, отражающие сущность и назначение
- Избегайте сокращений, кроме общепринятых (URL, ID, API)
- Следуйте единому стилю именования во всём проекте
- Добавляйте семантические префиксы для улучшения контекста

### 2.2. Именование с семантическими метками

#### Компоненты (Frontend)

```typescript
// Структура: [ТипКомпонента][ОбластьПрименения][Назначение]
const SitemapParserForm = () => { ... }          // Форма парсера sitemap
const PageSelectionTable = () => { ... }          // Таблица выбора страниц
const BlockSelectorModal = () => { ... }           // Модальное окно выбора блоков
const ParsingConfigPanel = () => { ... }           // Панель конфигурации парсинга
const TaskMonitoringDashboard = () => { ... }      // Дашборд мониторинга задач
```

#### Функции (Backend)

```python
# Структура: [Действие][Сущность][Контекст]
def parse_sitemap_from_url(url: str) -> dict:      # Парсинг sitemap из URL
def extract_page_content(html: str, rules: list) -> dict:  # Извлечение контента страницы
def apply_css_selectors(dom: object, selectors: dict) -> dict:  # Применение CSS-селекторов
def save_parsed_data_to_mongodb(data: dict, collection: str) -> str:  # Сохранение данных в MongoDB
def monitor_task_progress(task_id: str) -> dict:  # Мониторинг прогресса задачи
```

#### Переменные

```python
# Структура: [ТипДанных][Назначение][ДопИнформация]
sitemap_url_list = []                              # Список URL из sitemap
parsing_config_dict = {}                          # Конфигурация парсинга
selected_page_ids_set = set()                     # Набор ID выбранных страниц
css_selector_mapping = {}                          # Маппинг CSS-селекторов
task_progress_percentage = 0.0                     # Процент выполнения задачи
```

#### Классы и модели данных

```python
# Структура: [Сущность][Модель/Сервис/Репозиторий]
class SitemapParsingTask:                         # Модель задачи парсинга sitemap
class PageExtractionRule:                          # Модель правила извлечения страницы
class MongoDataRepository:                         # Репозиторий данных MongoDB
class ParsingWorkerService:                        # Сервис воркера парсинга
class TaskMonitoringService:                       # Сервис мониторинга задач
```

## 3. Конвенции комментирования кода

### 3.1. Формат документации функций

```python
def parse_sitemap_from_url(url: str, timeout: int = 30) -> dict:
    """
    Парсит sitemap по указанному URL.
    
    SEMANTIC: Функция извлечения структуры сайта из sitemap.xml
    
    Args:
        url (str): URL sitemap файла (может быть .xml или .xml.gz)
        timeout (int): Таймаут запроса в секундах
        
    Returns:
        dict: Словарь с результатами парсинга:
            - 'urls': List[str] - список найденных URL
            - 'is_index': bool - является ли файл индексом
            - 'child_sitemaps': List[str] - дочерние sitemap (если индекс)
            
    Raises:
        SitemapParseError: При ошибке парсинга XML
        TimeoutError: При превышении таймаута запроса
        
    Example:
        >>> result = parse_sitemap_from_url("https://example.com/sitemap.xml")
        >>> print(f"Найдено URL: {len(result['urls'])}")
    """
```

### 3.2. Семантические метки в комментариях

```python
# SEMANTIC: Инициализация конфигурации парсера по умолчанию
default_parsing_config = {
    "min_delay": 1.0,      # SEMANTIC: Минимальная задержка между запросами
    "max_delay": 3.0,      # SEMANTIC: Максимальная задержка между запросами
    "timeout": 30,         # SEMANTIC: Таймаут HTTP запроса
    "retries": 3,          # SEMANTIC: Количество попыток повтора
}

# SEMANTIC: Обработка результатов парсинга страницы
def process_parsed_page(page_url: str, extracted_data: dict) -> None:
    # SEMANTIC: Валидация извлеченных данных
    if not extracted_data.get('title'):
        logger.warning(f"Отсутствует заголовок для страницы: {page_url}")
    
    # SEMANTIC: Сохранение в MongoDB с обработкой дубликатов
    save_with_duplicate_handling(page_url, extracted_data)
```

### 3.3. Комментарии для сложных алгоритмов

```python
def generate_css_selector(element) -> str:
    """
    Генерирует уникальный CSS-селектор для DOM-элемента.
    
    SEMANTIC: Алгоритм создания селектора с максимальной специфичностью
    при минимальной длине для устойчивости к изменениям структуры страницы.
    """
    # SEMANTIC: Проверка наличия уникального ID - наиболее надежный селектор
    if element.get('id'):
        return f"#{element['id']}"
    
    # SEMANTIC: Построение пути на основе структуры DOM
    path_parts = []
    current = element
    
    # SEMANTIC: Подъем по DOM-дереву до body с сбором информации о тегах
    while current and current.get('tag') != 'body':
        tag = current['tag']
        
        # SEMANTIC: Добавление классов для повышения специфичности
        if current.get('classes'):
            tag += '.' + '.'.join(current['classes'])
        
        # SEMANTIC: Добавление индекса среди соседей для уникальности
        siblings = [sib for sib in current.get('siblings', []) 
                   if sib.get('tag') == current['tag']]
        if len(siblings) > 1:
            index = siblings.index(current) + 1
            tag += f":nth-of-type({index})"
        
        path_parts.append(tag)
        current = current.get('parent')
    
    # SEMANTIC: Реверс пути и формирование итогового селектора
    return ' > '.join(reversed(path_parts))
```

## 4. Структура метаданных для функций и классов

### 4.1. Метаданные для API эндпоинтов

```python
@app.post("/sitemaps/parse", tags=["sitemap"])
async def parse_sitemap_endpoint(
    request: SitemapParseRequest,
    current_user: User = Depends(get_current_user)
) -> SitemapParseResponse:
    """
    API эндпоинт для запуска парсинга sitemap.
    
    SEMANTIC: Инициация асинхронной задачи парсинга структуры сайта
    
    METADATA:
        - endpoint_type: async_task_initiator
        - authentication_required: true
        - rate_limit: 10/minute
        - response_time: <2s
        - cache_ttl: 0
    """
```

### 4.2. Метаданные для моделей данных

```python
class ParsingTask(BaseModel):
    """
    Модель задачи парсинга сайта.
    
    SEMANTIC: Основная сущность для хранения конфигурации и состояния задачи парсинга
    """
    id: Optional[str] = Field(None, description="Уникальный идентификатор задачи")
    sitemap_url: str = Field(..., description="URL sitemap для парсинга")
    status: TaskStatus = Field(TaskStatus.SCHEDULED, description="Текущий статус задачи")
    config: ParsingConfig = Field(..., description="Конфигурация параметров парсинга")
    
    # METADATA:
    #   collection_name: "tasks"
    #   indexes: ["sitemap_url", "status", "created_at"]
    #   ttl_field: "expires_at"
    
    class Config:
        schema_extra = {
            "example": {
                "sitemap_url": "https://example.com/sitemap.xml",
                "status": "scheduled",
                "config": {
                    "min_delay": 1.0,
                    "max_delay": 3.0,
                    "timeout": 30
                }
            }
        }
```

### 4.3. Метаданные для сервисов

```python
class PageParsingService:
    """
    Сервис парсинга страниц по правилам.
    
    SEMANTIC: Основной бизнес-логик извлечения данных из HTML по CSS-селекторам
    
    METADATA:
        - service_type: core_business_logic
        - dependencies: [HTTPClient, CSSSelectorEngine, MongoRepository]
        - transaction_scope: page_level
        - error_handling: retry_with_backoff
    """
    
    def __init__(self, http_client: HTTPClient, css_engine: CSSSelectorEngine, 
                 mongo_repo: MongoRepository):
        # SEMANTIC: Внедрение зависимостей для модульности и тестируемости
        self.http_client = http_client
        self.css_engine = css_engine
        self.mongo_repo = mongo_repo
```

## 5. Примеры семантической разметки для разных типов кода

### 5.1. API эндпоинты

```python
# SEMANTIC: Контроллер обработки sitemap
@router.post("/parse", response_model=SitemapParseResponse)
async def parse_sitemap(
    request: SitemapParseRequest,
    background_tasks: BackgroundTasks,
    db: Database = Depends(get_database)
):
    """
    Запускает парсинг sitemap.
    
    SEMANTIC: Создание фоновой задачи для асинхронной обработки sitemap
    
    METADATA:
        - endpoint_category: task_creation
        - async_processing: true
        - expected_response_time: <500ms
        - success_rate_target: >99%
    """
    # SEMANTIC: Валидация входных данных
    if not is_valid_sitemap_url(request.url):
        raise HTTPException(status_code=400, detail="Некорректный URL sitemap")
    
    # SEMANTIC: Создание задачи в базе данных
    task_id = await create_parsing_task(db, request.url, request.config)
    
    # SEMANTIC: Добавление фоновой задачи для обработки
    background_tasks.add_task(process_sitemap_task, task_id)
    
    return {"task_id": task_id, "status": "scheduled"}
```

### 5.2. Модели данных

```python
# SEMANTIC: Модель правила извлечения данных со страницы
class ExtractionRule(BaseModel):
    """
    Правило извлечения данных с веб-страницы.
    
    SEMANTIC: Конфигурация CSS-селектора и типа извлекаемых данных
    """
    name: str = Field(..., description="Семантическое имя правила")
    css_selector: str = Field(..., description="CSS-селектор для извлечения")
    content_type: ContentType = Field(..., description="Тип извлекаемого контента")
    attribute_name: Optional[str] = Field(None, description="Имя атрибута (если нужно)")
    is_multiple: bool = Field(False, description="Извлекать множественные значения")
    
    # METADATA:
    #   validation_rules: ["css_selector_syntax", "attribute_exists_if_specified"]
    #   example_usage: "product_title extraction from e-commerce pages"
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "name": "product_title",
                "css_selector": "h1.product-title",
                "content_type": "text",
                "is_multiple": false
            }
        }
```

### 5.3. Сервисы

```python
# SEMANTIC: Сервис обработки очереди задач парсинга
class TaskQueueService:
    """
    Сервис управления очередью задач парсинга.
    
    SEMANTIC: Оркестрация выполнения задач с учетом приоритетов и ресурсов
    
    METADATA:
        - service_pattern: queue_processor
        - concurrency_model: async_worker_pool
        - scaling_strategy: dynamic_based_on_load
        - monitoring_required: true
    """
    
    async def process_task_queue(self):
        """
        Основной цикл обработки очереди задач.
        
        SEMANTIC: Бесконечный цикл извлечения и выполнения задач
        
        METADATA:
            - execution_pattern: event_loop
            - error_handling: graceful_degradation
            - performance_metrics: ["queue_length", "processing_time", "success_rate"]
        """
        while True:
            # SEMANTIC: Получение следующей задачи с учетом приоритета
            task = await self.get_next_task()
            
            if task:
                # SEMANTIC: Делегирование выполнения соответствующему обработчику
                await self.delegate_task_execution(task)
            else:
                # SEMANTIC: Задержка при пустой очереди для экономии ресурсов
                await asyncio.sleep(1)
```

### 5.4. Компоненты React

```typescript
/**
 * Комponent выбора CSS-селекторов на странице.
 * 
 * SEMANTIC: Интерактивный компонент для визуального выбора DOM-элементов
 * и автоматической генерации CSS-селекторов
 * 
 * METADATA:
 * - component_type: interactive_selector
 * - dependencies: [iframe, css_selector_generator, highlight_overlay]
 * - user_interaction: [click, hover, keyboard_navigation]
 */
const BlockSelectorComponent: React.FC<BlockSelectorProps> = ({ 
  pageUrl, 
  onSelectorGenerated 
}) => {
  // SEMANTIC: Состояние выбранного элемента для подсветки
  const [selectedElement, setSelectedElement] = useState<DOMElement | null>(null);
  
  // SEMANTIC: Состояние режима выбора (активен/неактивен)
  const [isSelectionMode, setIsSelectionMode] = useState<boolean>(false);
  
  /**
   * Обработчик клика по элементу в iframe.
   * 
   * SEMANTIC: Генерация CSS-селектора для кликнутого элемента
   * 
   * @param event - событие клика с информацией об элементе
   */
  const handleElementClick = useCallback((event: ElementClickEvent) => {
    // SEMANTIC: Генерация устойчивого CSS-селектора
    const selector = generateCSSSelector(event.element);
    
    // SEMANTIC: Обновление состояния выбранного элемента
    setSelectedElement(event.element);
    
    // SEMANTIC: Уведомление родительского компонента о сгенерированном селекторе
    onSelectorGenerated({
      name: `selector_${Date.now()}`,
      cssSelector: selector,
      elementType: event.element.tagName.toLowerCase()
    });
  }, [onSelectorGenerated]);
  
  return (
    <div className="block-selector-container">
      {/* SEMANTIC: Панель управления режимом выбора */}
      <div className="selector-controls">
        <button 
          onClick={() => setIsSelectionMode(!isSelectionMode)}
          className={`selection-mode-btn ${isSelectionMode ? 'active' : ''}`}
        >
          {isSelectionMode ? 'Выключить выбор' : 'Включить выбор'}
        </button>
      </div>
      
      {/* SEMANTIC: Iframe с загруженной страницей для выбора элементов */}
      <iframe
        src={pageUrl}
        className="page-preview-frame"
        onLoad={handleIframeLoad}
        sandbox="allow-same-origin allow-scripts"
      />
      
      {/* SEMANTIC: Информационная панель с данными о выбранном элементе */}
      {selectedElement && (
        <ElementInfoPanel element={selectedElement} />
      )}
    </div>
  );
};
```

## 6. Рекомендации по структурированию кода

### 6.1. Организация файловой структуры

```
src/
├── backend/
│   ├── api/                    # SEMANTIC: Определения API эндпоинтов
│   │   ├── v1/
│   │   │   ├── sitemap.py      # SEMANTIC: Эндпоинты для работы с sitemap
│   │   │   ├── tasks.py        # SEMANTIC: Эндпоинты управления задачами
│   │   │   └── pages.py        # SEMANTIC: Эндпоинты работы со страницами
│   │   └── dependencies.py    # SEMANTIC: Общие зависимости API
│   ├── core/                   # SEMANTIC: Основная бизнес-логика
│   │   ├── parsing/            # SEMANTIC: Модули парсинга
│   │   │   ├── sitemap_parser.py
│   │   │   ├── page_parser.py
│   │   │   └── selector_engine.py
│   │   ├── storage/            # SEMANTIC: Модули хранения данных
│   │   │   ├── mongodb.py
│   │   │   └── models.py
│   │   └── services/           # SEMANTIC: Сервисы бизнес-логики
│   │       ├── task_service.py
│   │       └── queue_service.py
│   └── utils/                  # SEMANTIC: Вспомогательные утилиты
│       ├── http_client.py
│       └── validators.py
└── frontend/
    ├── components/             # SEMANTIC: Переиспользуемые компоненты UI
    │   ├── common/             # SEMANTIC: Общие компоненты
    │   ├── parsing/            # SEMANTIC: Компоненты для парсинга
    │   └── monitoring/         # SEMANTIC: Компоненты мониторинга
    ├── pages/                  # SEMANTIC: Компоненты страниц
    ├── services/               # SEMANTIC: Сервисы для работы с API
    ├── hooks/                  # SEMANTIC: Кастомные React хуки
    └── utils/                  # SEMANTIC: Вспомогательные функции
```

### 6.2. Принципы организации кода

1. **Разделение ответственности**: Каждый модуль должен иметь четкую семантическую зону ответственности
2. **Инкапсуляция**: Скрытие деталей реализации за семантически понятными интерфейсами
3. **Минимальные зависимости**: Уменьшение связанности между модулями
4. **Тестируемость**: Структурирование кода для удобства модульного тестирования

### 6.3. Семантическое группирование функций

```python
# SEMANTIC: Группа функций для работы с sitemap
class SitemapProcessor:
    """Класс для обработки sitemap файлов."""
    
    # SEMANTIC: Функции загрузки
    async def download_sitemap(self, url: str) -> bytes: ...
    async def download_gzipped_sitemap(self, url: str) -> bytes: ...
    
    # SEMANTIC: Функции парсинга
    def parse_sitemap_xml(self, content: bytes) -> dict: ...
    def parse_sitemap_index(self, content: bytes) -> dict: ...
    
    # SEMANTIC: Функции валидации
    def validate_sitemap_structure(self, sitemap_data: dict) -> bool: ...
    def validate_url_format(self, url: str) -> bool: ...
```

### 6.4. Семантическое именование тестов

```python
# SEMANTIC: Тесты для модуля парсинга sitemap
class TestSitemapParser:
    """Тесты класса SitemapParser."""
    
    # SEMANTIC: Тесты базового функционала
    def test_parse_simple_sitemap_returns_correct_urls(self): ...
    def test_parse_sitemap_index_returns_child_sitemaps(self): ...
    
    # SEMANTIC: Тесты обработки ошибок
    def test_parse_invalid_xml_raises_sitemap_parse_error(self): ...
    def test_parse_unreachable_url_raises_timeout_error(self): ...
    
    # SEMANTIC: Тесты пограничных случаев
    def test_parse_empty_sitemap_returns_empty_list(self): ...
    def test_parse_huge_sitemap_respects_url_limit(self): ...
```

## 7. Интеграция с ИИ-ассистентами

### 7.1. Специальные комментарии для ИИ

```python
# AI_INSTRUCTION: При рефакторинге этой функции сохраните обратную совместимость
def extract_data_with_rules(html_content: str, rules: List[ExtractionRule]) -> dict:
    ...

# AI_INSTRUCTION: Этот код требует оптимизации для больших объемов данных
# TODO_AI: Рассмотреть возможность асинхронной обработки
def process_large_dataset(dataset: List[dict]) -> List[dict]:
    ...

# AI_INSTRUCTION: Этот класс является критичным для безопасности, не изменяйте валидацию
class SecurityValidator:
    ...
```

### 7.2. Семантические маркеры для автоматического анализа

```python
# SEMANTIC_MARKER: high_complexity_algorithm
def complex_parsing_algorithm(data: dict) -> dict:
    ...

# SEMANTIC_MARKER: performance_critical
def performance_critical_function():
    ...

# SEMANTIC_MARKER: security_sensitive
def handle_user_input(input_data: str):
    ...
```

## 8. Заключение

Следование данным рекомендациям по семантической разметке кода позволит:

1. Улучшить понимание кода ИИ-ассистентами
2. Ускорить разработку и рефакторинг
3. Повысить качество автоматической генерации кода
4. Упростить онбординг новых разработчиков
5. Обеспечить консистентность кодовой базы

Регулярное обновление данного руководства и адаптация под новые требования проекта помогут поддерживать высокое качество семантической разметки на протяжении всего жизненного цикла проекта.