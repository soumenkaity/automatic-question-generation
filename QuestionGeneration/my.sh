#/usr/bin/env bash

java -Xmx1200m -cp question-generation.jar edu.cmu.ark.StanfordParserServer --grammar config/englishFactored.ser.gz --port 5556 --maxLength 40 &
java -Xmx500m -cp lib/supersense-tagger.jar edu.cmu.ark.SuperSenseTaggerServer  --port 5557 --model config/superSenseModelAllSemcor.ser.gz --properties config/QuestionTransducer.properties