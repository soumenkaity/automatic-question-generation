echo "inside runscript.sh"
cd /home/cgi/Project/question-generation/QuestionGeneration
echo "$1"
bash my.sh &
python3 ../question.py -p "$1"