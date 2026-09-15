# Índex de les diferents instruccions per agents

En aquest arxiu es llisten els diferents documents amb instruccions per a agents de Copilot Xat.

## Instruccions definitives

Aquestes són les que han donat un bon resultat.

### Assistent CQS SAIEP

- Assistent per a la plataforma de consultes, queixes i suggeriments del Servei d’Autorització d’Instal·lacions Elèctriques de Producció.

En la versió definitiva, les instruccions es caracteritzen per:

- No inclouen cap mena de font (ni tan sols enllaços). S'espera que l'usuari proporcioni les fonts en documents.

- Les fonts s'espera que siguin:

    - Les FAQs del Servei

    - Un resum dels tràmits disponibles

    - Una blacklist per filtrar consultes

- L'objectiu és generar un esbós de resposta per a una consulta ciutadana.

- L'assistent segueix 5 passos per tal d'entendre, filtrar i respondre la consulta.

- El format de la resposta es divideix clarament en 2 parts: raonament i resposta al ciutadà. Es fa servir *chain of thought prompting* per potencialment millorar la resposta i evitar errors.

- Hi ha *fallbacks* per a les consultes que no s'han de respondre.


[./instruccions_assistent_cqs_saiep.md](./instruccions_assistent_cqs_saiep.md)

### Assistent de reescriptura de FAQs

Aquest assistent s'ha fet servir per agilitzar el procés de reescriptura de les FAQ.

En proporcionar-li una FAQ i demanar-li que la millori, fa la resposta més entenedora i li dona una estructura a vegades més esquemàtica, tot mantenint el rigor tècnic i legal.

[./instruccions_reescriptor_faqs.md](./instruccions_reescriptor_faqs.md)

## Proves inicials i instruccions millorables

Aquestes són les que s'han provat, però han donat resultats dolents o millorables. Totes són per a l'assistent de consultes de CQS en versions o enfocaments anteriors.


### Primeres versions de l'assistent de consultes

Les primeres versions es caracteritzen per:

- Les fonts d'informació es donen com a enllaços a web dins les instruccions. No es pot fer posant aquests enllaços a la configuració de l'agent perquè els enllaços tenen més de dos nivells de profunditat.

- Les instruccions estan en anglès, per tal d’aprofitar que és la llengua predominant en les dades d’entrenament, i que, simplificant molt, es pot entendre que els models aprenen en una "llengua" més semblant a l’anglès que a altres.

- El format és text simple.

- Hi ha casos de *fallback* per consultes que no s'han de respondre.


#### Agent de generació de respostes

Aquestes instruccions sorgeixen d’una proposta inicial revisada amb el Prompt Coach, un assistent de Microsoft que serveix per millorar consultes. S’ha fet servir few-shot prompting per millorar les respostes. 

[./proves_inicials/instruccions_generacio_cqs_inicial.md](./proves_inicials/instruccions_generacio_cqs_inicial.md)


#### Agent de verificació de respostes

Per a aquest objectiu, ha sigut necessari incloure més documents legislatius que a l'agent de generació de respostes, el que potencialment pot degradar el rendiment. S’ha basat en les instruccions de l’altre objectiu i s’ha millorat lleugerament amb el Prompt Coach.

[./proves_inicials/instruccions_verificacio_cqs_inicial.md](./proves_inicials/instruccions_verificacio_cqs_inicial.md)


### Assistent de cerca de consultes

Aquest assistent té un objectiu simplificat: en lloc de fer respostes, simplement cerca a les fonts les FAQ similars i en fa una llista.

Hi ha diferències importants respecte a les proves inicials:

- Les fonts d'informació no es donen com a webs. La cerca a web està desactivada i l'agent espera que l'usuari proporcioni les fonts d'informació, sigui al *prompt* o adjuntant un document.

- S'han fet unes instruccions molt més específiques. Es comença a intuir un procés de treball per passos.

- El format és més ric: s'usen títols i subtítols, i les instruccions se separen en diferents seccions concretes.

- S'ha optat per fer-les en català per permetre a tot el personal de la Generalitat que pugui llegir-les. Això és més important que el possible guany de rendiment que doni l'anglès.

[./proves_inicials/instruccions_cerca_cqs.md](./proves_inicials/instruccions_cerca_cqs.md)

S'ha millorat, afegint la nova *blacklist* a les instruccions, nous *fallbacks* i refinant el format de la resposta.

[./proves_inicials/instruccions_cerca_cqs2.md](./proves_inicials/instruccions_cerca_cqs2.md)

Aquestes es van millorar per aconseguir les definitives, que trobareu més amunt. D'entre els canvis es destaca:

- Demanar a l'agent que generés respostes, no simplement que cerqués FAQ.

- Detallar el procés de treball en passos.

- Detallar el format de la resposta.

- Detallar els casos especials i de *fallback*.

- Ampliar les regles de qualitat.

- Moure la *blacklist* al document de fonts d'informació.

- Eliminar els exemples de consultes, ja que com tampoc no tenien respostes, no era un *few-shot prompting* correcte, el que hauria ocupat massa espai de les instruccions.