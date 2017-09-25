# planet-express
Auto relational searcher for political documents in Spain


# The problem
if you wanna search a timeline relation of a law or an parlamentary iniciative between goberments pages and public pages is very difficult and manual to search it.

We try to propose a tool that from a text search you can get these relations.

## Example

Ley sinde was a part of a law to regulate the compensation for copyright to the autors in Spain, if you find "Ley sinde" in the medias you get a lot of results.

For example in https://elpais.com/buscador/ you have 1059 results

But if you want to search this law in congreso.es in the IX legislature for "Ley de Economía Sostenible", ley sinde is an apart of this  law, in the search you get information about questions in the congress and meetings about this law.

So, if in we have all the documents from elpais and congreso about this law, our system should be offer the documents relationated between then with a weight to detect what documents has a more important relation.


### How to get a relation?

In basics we work with text, so the relations are with the relation between these text, this relations could be of differents types:
 - exactly text: "ley sinde" is equal to "ley sinde"
 - important words: "Los DERECHOS de explotación relativos a la propiedad intelectual corresponderán a
las entidades en que el AUTOR haya desarrollado una relación de servicios, en los términos
y con el alcance previsto en la legislación sobre propiedad intelectual." matching with "Los DERECHOS de AUTOR podran ser reclamados por la sgae" 
- third relations: "Los derechos de explotación relativos por DERECHOS DE AUTOR" -> "el CANON impuesto por DERECHOS DE AUTOR" -> "CEDRO reclama una subida del CANON por COPYRIGHT"
- url relations: thir is directly in the document but you can't skip it
- dates: maybe this is a kind of exactly text, but is very important because these documents the media publish information when this this is relevant, and this is indicate by the date, soy maybe two documents talking about the same but one during the votation in the congress and another a few month ago, the first is most important.
- names: the people who work or are relationated with the topic of the documents is very important overall in politics.

