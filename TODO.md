# TODO - Correções Críticas para Produção - Clone X

## ✅ Já Implementado
- [x] Configuração de banco de dados com dj-database-url
- [x] Sistema de logs com RotatingFileHandler
- [x] Configurações de segurança SSL e HSTS
- [x] Configurações de email
- [x] Validador customizado de senha no AUTH_PASSWORD_VALIDATORS
- [x] Otimização de queries com select_related e prefetch_related
- [x] Índices de banco de dados em campos críticos
- [x] Sistema de cache básico configurado
- [x] Configuração de arquivos estáticos para produção
- [x] Testes abrangentes para models e views

## 🔴 Crítico - Deve ser Corrigido Imediatamente

### 1. Validação de Senha Inconsistente
- [x] Remover função duplicada `validate_strong_password` em `users/forms.py`
- [x] Garantir que apenas o validador customizado seja usado

### 2. Validação de Upload de Imagens
- [x] Adicionar validação de tipo/extensão em `posts/models.py`
- [x] Prevenir upload de arquivos maliciosos

### 3. Duplicação de Código em Views
- [x] Corrigir duplicação entre `core/views.py` e `posts/views.py`
- [x] Unificar lógica de feed

### 4. Testes Insuficientes
- [x] Adicionar testes para posts (Comment, Like)
- [x] Adicionar testes de integração
- [x] Testar validações de formulário

### 5. Otimização de Queries (N+1 Problem)
- [x] Adicionar `prefetch_related` para likes/comments no feed
- [x] Otimizar queries de busca de usuários

### 6. Índices de Banco de Dados
- [x] Adicionar índices em campos de busca (username, email, created_at)

### 7. Sistema de Cache
- [x] Implementar cache básico para queries frequentes

### 8. Configuração de Arquivos Estáticos
- [x] Verificar configuração de static files para produção

## 🟡 Médio Prioridade

### 9. Segurança Extra
- [ ] Adicionar rate limiting básico
- [ ] Melhorar validação de CSRF

### 10. Performance
- [ ] Implementar paginação com cursor se necessário
- [ ] Otimizar processamento de imagens

## 🟢 Baixo Prioridade

### 11. Monitoramento
- [ ] Adicionar métricas básicas
- [ ] Health checks

### 12. Documentação
- [ ] Atualizar README com novas configurações
- [ ] Documentar variáveis de ambiente

## 📋 Plano de Implementação

1. **Fase 1 - Crítico**: Correções que impedem deploy seguro
2. **Fase 2 - Médio**: Melhorias de performance e segurança
3. **Fase 3 - Baixo**: Monitoramento e documentação
4. **Testes**: Testar todas as mudanças
5. **Revisão Final**: Verificar se tudo está em ordem
