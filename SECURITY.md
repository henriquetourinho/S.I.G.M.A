# 🔐 Política de Segurança – S.I.G.M.A.

Este documento descreve as práticas de segurança adotadas pelo projeto [S.I.G.M.A.](https://github.com/henriquetourinho/S.I.G.M.A), bem como orientações para reporte responsável de vulnerabilidades.

---

## 🛡️ Visão Geral

O S.I.G.M.A. é uma aplicação de desktop para exploração e mapeamento de arquivos locais, desenvolvida em Python com PySide6. A aplicação lida com leitura massiva de arquivos, metadados e permissões do sistema de arquivos, podendo ser executada com permissões elevadas dependendo do contexto de uso.

Por envolver acesso a informações sensíveis do sistema, a atenção à segurança é fundamental.

---

## ✅ Boas Práticas Recomendadas

Antes de executar o S.I.G.M.A., recomenda-se:

- ✅ **Audite o código-fonte** localmente (100% open-source).
- ✅ **Evite executar como root**. Prefira rodar como usuário normal, exceto onde estritamente necessário.
- ✅ **Faça backups** dos dados sensíveis que possam ser acessados ou exibidos pela ferramenta.
- ✅ **Use preferencialmente em ambientes de teste** ou homologação antes de adotar em ambientes de produção.
- ✅ **Mantenha seu sistema operacional e dependências atualizados**, aplicando sempre os patches de segurança recomendados.

---

## ⚠️ Possíveis Riscos Identificados

O uso inadequado, permissões excessivas ou alterações impróprias do S.I.G.M.A. podem causar:

- ❗ Vazamento ou exposição acidental de informações sensíveis do sistema de arquivos.
- ❗ Listagem ou leitura de arquivos protegidos, caso seja rodado como root.
- ❗ Sobrecarga do sistema ao escanear grandes volumes de dados sem critérios de filtro adequados.
- ❗ Modificações não documentadas podem introduzir falhas ou abrir vetores de ataque.

---

## 📬 Reporte de Vulnerabilidades

Se você identificar falhas de segurança, comportamentos suspeitos ou vulnerabilidades no S.I.G.M.A., siga os passos abaixo:

1. **Não abra uma _issue_ pública imediatamente.**
2. Entre em contato diretamente via e-mail:
   - 📧 **henriquetourinho@riseup.net**
3. Inclua:
   - Sistema operacional e versão
   - Passos para reprodução
   - Logs, saídas, prints ou demonstrações (se possível)

Todos os relatos serão tratados com confidencialidade e prioridade máxima.

---

## 📦 Política de Correções

- 🛠️ Correções para problemas de segurança terão prioridade máxima no ciclo de atualizações.
- 🔁 Melhorias de segurança serão incorporadas continuamente nas versões subsequentes.
- 📄 Um `CHANGELOG.md` é mantido com registros de alterações, incluindo patches de segurança.

---

## 🧠 Contribuições e Agradecimentos

A segurança do S.I.G.M.A. é responsabilidade de toda a comunidade. Contribuições para análise de segurança, sugestões de melhorias e _pull requests_ são sempre bem-vindos!

[Abra uma Pull Request](https://github.com/henriquetourinho/S.I.G.M.A/pulls)

---

> 💬 Para dúvidas gerais, use a aba [Discussions](https://github.com/henriquetourinho/S.I.G.M.A/discussions).
>
> 🚨 Para alertas confidenciais, utilize **henriquetourinho@riseup.net**

---

**Carlos Henrique Tourinho Santana**  
Mantenedor do Projeto S.I.G.M.A.  
[GitHub: @henriquetourinho](https://github.com/henriquetourinho)