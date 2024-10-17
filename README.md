## PICCOLO ORM
### Создание миграций
```bash
piccolo migrations new my_app
piccolo migrations new my_app --auto
```

### Применение миграций
```bash
piccolo migrations forwards my_app
piccolo migrations forwards all
```

### Отмена миграций
```bash
piccolo migrations backwards my_app 2022-09-04T19:44:09
```

### Проверка миграций
```bash
piccolo migrations check
```
