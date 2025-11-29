# 📚 Guia Rápido - Git para Chemical Pharma

## ✅ Status Atual
- ✅ Repositório Git inicializado
- ✅ `.gitignore` configurado
- ✅ Commit inicial realizado (32 arquivos, ~10.000 linhas)
- ✅ README.md criado e commitado

## 🔄 Comandos Básicos do Git

### Ver o Status do Projeto
```bash
git status
```
Mostra arquivos modificados, adicionados ou deletados.

### Ver Histórico de Commits
```bash
git log --oneline
git log --graph --oneline --all  # Com gráfico visual
```

### Salvar Alterações (Fazer um Commit)

**1. Adicionar arquivos ao staging:**
```bash
git add .                    # Adiciona todos os arquivos
git add backend/app.py       # Adiciona arquivo específico
git add backend/             # Adiciona pasta inteira
```

**2. Fazer o commit:**
```bash
git commit -m "Descrição das mudanças"
```

**Exemplo completo:**
```bash
git add .
git commit -m "feat: Add pentagon particle support"
```

### Ver Diferenças (O Que Mudou)
```bash
git diff                     # Ver mudanças não adicionadas
git diff --staged            # Ver mudanças já no staging
git diff HEAD~1              # Comparar com commit anterior
```

### Desfazer Mudanças

**Descartar mudanças em um arquivo (CUIDADO!):**
```bash
git checkout -- backend/app.py
```

**Remover arquivo do staging:**
```bash
git reset backend/app.py
```

**Desfazer último commit (mantém alterações):**
```bash
git reset --soft HEAD~1
```

### Branches (Ramificações)

**Criar e usar branches para experimentar:**
```bash
git branch nova-feature       # Criar branch
git checkout nova-feature     # Mudar para a branch
git checkout -b nova-feature  # Criar e mudar (atalho)

# Trabalhar na branch...
git add .
git commit -m "Testando nova feature"

# Voltar para master
git checkout master

# Mesclar a branch (se deu certo)
git merge nova-feature

# Deletar a branch
git branch -d nova-feature
```

## 🎯 Fluxo de Trabalho Recomendado

### Ao Iniciar o Dia
```bash
git status                    # Ver se há mudanças pendentes
```

### Durante o Desenvolvimento
```bash
# A cada funcionalidade completa:
git add .
git commit -m "feat: Descrição da funcionalidade"

# A cada bug corrigido:
git add .
git commit -m "fix: Descrição do bug corrigido"

# A cada melhoria:
git add .
git commit -m "refactor: Descrição da melhoria"
```

### Antes de Experimentar Algo Arriscado
```bash
# Criar uma branch para testar
git checkout -b teste-arriscado

# Fazer as mudanças...

# Se deu certo:
git checkout master
git merge teste-arriscado
git branch -d teste-arriscado

# Se deu errado:
git checkout master
git branch -D teste-arriscado  # Descartar tudo
```

## 📝 Convenções de Commit

Use prefixos para organizar commits:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `refactor:` - Melhoria de código (sem mudar funcionalidade)
- `docs:` - Documentação
- `style:` - Formatação, estilo (não afeta lógica)
- `test:` - Adicionar testes
- `chore:` - Tarefas de manutenção

**Exemplos:**
```bash
git commit -m "feat: Add multiple molecules support in synthesis"
git commit -m "fix: Solve commutativity issue in synthesis algorithm"
git commit -m "refactor: Improve rebond algorithm performance"
git commit -m "docs: Update README with new features"
```

## 🆘 Comandos de Emergência

### "Perdi um arquivo!"
```bash
git checkout HEAD -- nome-do-arquivo.py
```

### "Quero voltar para o commit anterior!"
```bash
git log --oneline              # Copiar o hash do commit
git checkout abc1234           # Voltar para esse commit (modo detached)
git checkout master            # Voltar para o presente
```

### "Commitei algo errado!"
```bash
# Se ainda não compartilhou com ninguém:
git reset --soft HEAD~1        # Desfaz commit, mantém mudanças
git reset --hard HEAD~1        # Desfaz commit, REMOVE mudanças (CUIDADO!)
```

## 🌐 Backup Remoto (GitHub/GitLab)

### Configurar Repositório Remoto
```bash
# Criar repositório no GitHub/GitLab primeiro, depois:
git remote add origin https://github.com/seu-usuario/chemical-pharma.git
git push -u origin master
```

### Enviar Mudanças
```bash
git push
```

### Baixar Mudanças
```bash
git pull
```

## 📊 Visualizar o Projeto

### Ver Arquivos Versionados
```bash
git ls-files
```

### Ver Tamanho do Repositório
```bash
git count-objects -vH
```

### Ver Estatísticas
```bash
git shortlog -sn              # Commits por autor
```

## 🎓 Dicas Importantes

1. **Faça commits pequenos e frequentes** - Mais fácil de entender e reverter
2. **Use mensagens descritivas** - "fix bug" é ruim, "fix: Solve pentagon bond count" é bom
3. **Commit antes de fazer algo arriscado** - Você pode sempre voltar
4. **Use branches para experimentar** - Master fica seguro
5. **Nunca use `--force` sem entender** - Pode perder dados
6. **`.gitignore` protege arquivos sensíveis** - Verifique antes de commitar

## 📞 Ajuda

```bash
git help                      # Lista de comandos
git help commit              # Ajuda sobre comando específico
```

---

**🎮 Agora seu projeto está protegido!** Você pode experimentar à vontade sabendo que sempre pode voltar atrás! 🚀


