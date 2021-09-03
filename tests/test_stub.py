from pyspark_k8s_boilerplate.jobs import pi

def test_pi():
	assert round(pi.execute(output=True)) == 3


def test_truth():
	assert True == True