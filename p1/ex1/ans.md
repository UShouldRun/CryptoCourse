**Q1.1**: Decrypt the ciphertext, and describe your methodology

In this exercise, the ciphertext will be deciphered using frequency analysis. This will involve trial and error and logic deduction.

The first step was to discover the most common English 3-gram *THE*. It should also be one of the most used 3-grams in the ciphertext, so it should be one of these:

```
3-gram (top 26):
pac: 8
usi: 8
bnd: 7
nai: 6
ndt: 6
```

The two most common 2-grams in English are *TH* and *HE*, which helps to narrow it down. If we see two 2-grams in our list which together make one of the most common 3-grams, it will probably be *THE*. This happens with *us* + *si* and *pa* + *ac*.

```
2-gram (top 26):
us: 15
ac: 15
ea: 13
ai: 11
ip: 10
re: 10
no: 9
pa: 9
si: 9
```

We first tried choosing *usi* -> *THE*, because the single letter frequency made more sense. Then *pac* -> *AND*, the next most common English 3-gram. This is how the ciphertext looked after that:

```
oEzETmnrEtdqEmTnfnqqnoTHATANDTHemTHEmEANDTHnmENnnNExNnomoEzETTHEmEweqqmTnmoAqqnoHnoTHEbmTehxeNbndtTHtnATTAmTEmqexEznqDnHoHATbndDnTnrENnnNExNnomANDetEAqeyEbndtEreNEeNDEEDAfnnqAreANDetEAqeyEbndtEreNEeNDEEDAfnnqAreeelndtNEbTHtndzHTHEDEmEtTnfTHEreNDoeTHNnHnwEefnqqnoeDtefTAqnNzTHEnhEANDEADqefEjnATeNTHEmdNANDhnrEdNDnNEwqEAmANTqbhAgeNeNehnrEdNDnNEANDetEAqeyEbndtEreNEeNDEEDAfnnqAreANDetEAqeyEbndtEreNEeNDEEDAfnnqAreeHEAgENmreqEmAjngErEoHATAzefTHEtEjEqnojdTNnnNExNnomAzefTTHATbndzegETnrENnnNExNnom
```

At this point, these were the most used letters in our text, and the matches they had, followed by the most common letters in English:

```
1-gram (top 26):
i: 69 -> E
n: 57 
a: 43 -> N
e: 42 
p: 37 -> A
u: 35 -> T

x  x  x        x     x 
E, T, A, O, I, N, S, H, R
```


By order of frequency, *O* and *I* should be the next to be chosen, so we tried swapping *n* -> *O* and *e* -> *I*

This is how the ciphertext looks after these changes:

```
oEzETmOrEtdqEmTOfOqqOoTHATANDTHImTHEmEANDTHOmENOONExNOomoEzETTHEmEwIqqmTOmoAqqOoHOoTHEbmTIhxINbOdtTHtOATTAmTEmqIxEzOqDOHoHATbOdDOTOrENOONExNOomANDItEAqIyEbOdtErINEINDEEDAfOOqArIANDItEAqIyEbOdtErINEINDEEDAfOOqArIIIlOdtNEbTHtOdzHTHEDEmEtTOfTHErINDoITHNOHOwEIfOqqOoIDtIfTAqONzTHEOhEANDEADqIfEjOATINTHEmdNANDhOrEdNDONEwqEAmANTqbhAgININIhOrEdNDONEANDItEAqIyEbOdtErINEINDEEDAfOOqArIANDItEAqIyEbOdtErINEINDEEDAfOOqArIIHEAgENmrIqEmAjOgErEoHATAzIfTHEtEjEqOojdTNOONExNOomAzIfTTHATbOdzIgETOrENOONExNOom
```

Looking at the ```THATANDTHImTHEmEANDTHOmE``` snippet, it seems probable that *m* -> *S*. Then ```NOONExNOoS```, appears a few times and looks like it could be ```No one knows```, so *x* -> *K* and *o* -> *W*.

Now these are the characters we were able to translate and the most common letters in English:

```
1-gram (top 26):
i: 69 E
n: 57 O
a: 43 N
e: 42 I
p: 37 A
u: 35 T
q: 25 
c: 24 D
s: 22 H
m: 20 S

x  x  x  x  x  x  x  x  x  x       
E, T, A, O, I, N, S, H, R, D, L, C, U
```

We tried *q* -> *L*, and there no immediate problems. Also there was the ```wLEASANT```, which might indicate *w* -> *P*


```
WEzETSOrEtdLESTOfOLLOWTHATANDTHISTHESEANDTHOSENOONEKNOWSWEzETTHESEPILLSTOSWALLOWHOWTHEbSTIhKINbOdtTHtOATTASTESLIKEzOLDOHWHATbOdDOTOrENOONEKNOWSANDItEALIyEbOdtErINEINDEEDAfOOLArIANDItEALIyEbOdtErINEINDEEDAfOOLArIIIlOdtNEbTHtOdzHTHEDESEtTOfTHErINDWITHNOHOPEIfOLLOWIDtIfTALONzTHEOhEANDEADLIfEjOATINTHESdNANDhOrEdNDONEPLEASANTLbhAgININIhOrEdNDONEANDItEALIyEbOdtErINEINDEEDAfOOLArIANDItEALIyEbOdtErINEINDEEDAfOOLArIIHEAgENSrILESAjOgErEWHATAzIfTHEtEjELOWjdTNOONEKNOWSAzIfTTHATbOdzIgETOrENOONEKNOWS
```

At this point, most of the common letters were already translated. After the harder work was done, we just had to logically substitute the remaining letters case by case, according to meaning of the text, resulting in the following plaintext:

```
WE GET SOME RULES TO FOLLOW THAT AND THIS THESE AND THOSE NO ONE KNOWS WE GET THESE PILLS TO SWALLOW HOW THEY STICK IN YOUR THROAT TASTES LIKE GOLD OH WHAT YOU DO TO ME NO ONE KNOWS AND I REALIZE YOURE MINE INDEED A FOOL AM I AND I REALIZE YOURE MINE INDEED A FOOL AM III JOURNEY THROUGH THE DESERT OF THE MIND WITH NO HOPE I FOLLOW I DRIFT ALONG THE OCEAN DEAD LIFEBOAT IN THE SUN AND COME UNDONE PLEASANTLY CAVIN IN I COME UNDONE AND I REALIZE YOURE MINE INDEED A FOOL AM I AND I REALIZE YOURE MINE INDEED A FOOL AM II HEAVENS MILES ABOVE ME WHAT A GIFT HERE BELOW BUT NO ONE KNOWS A GIFT THAT YOU GIVE TO ME NO ONE KNOWS
```