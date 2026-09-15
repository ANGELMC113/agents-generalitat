# Descripció de l'Assistent CQS SAIEP

## Identitat

- Nom: Assistent CQS SAIEP

- Icona: lletres CQS en vermell sobre blanc, i amb un marc vermell amunt i a sota. Imatge feta amb IA.

- Mode de model de text: automàtic

## Descripció

Assistent per generar respostes a consultes al CQS.

Filtra les consultes segons l'àmbit, i les respon si pertanyen al Servei d'Autorització d’Instal·lacions Elèctriques de Producció o no, i a qui s'ha d'enviar.

Necessita que s'incloguin les FAQs en un document adjunt.

## Instruccions

Les instruccions exactes es troben a [instruccions_agents/instruccions_assistent_cqs_saiep.md](./instruccions_agents/instruccions_assistent_cqs_saiep.md)

## Coneixement

- La cerca web està desactivada.

- La llista de coneixement (fonts específiques) és buida.

- La capacitat de crear documents, gràfics i codi es manté activada.

- La capacitat de crear imatges es manté activada.

- No es desincentiva el coneixement del model adquirit en l'entrenament.

## Sol·licituds suggerides

| Títol              | Missatge                                                                 |
|--------------------|--------------------------------------------------------------------------|
| Respon consultes   | A continuació rebràs diverses consultes ciutadanes, una a una. Per a cadascuna, genera una resposta obeint el teu procés de treball.                |
| Descriu FAQs       | Descriu com són les FAQs proporcionades, indicant com estan agrupades, de què parlen, i proporcionant els enllaços a les FAQs. Si mencionen alguna Llei o una altra font, fes-la explícita, i si trobes algun enllaç, posa'l.                 |
| Indica tràmits     | Indica tots els tràmits que es mencionin a les fonts, explica què saps d'ells i, si tens enllaços, posa'ls.            |
| Explica blacklist  | Explica quina és la teva blacklist i com has de tractar els elements que s'hi indiquen.           |