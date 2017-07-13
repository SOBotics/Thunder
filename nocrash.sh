result=1
while [ $result -ne 0 ]; do
	echo "---------------------------------"
	echo "Thunder started."
	echo "---------------------------------"
	python3 main.py
	result=$?
done
