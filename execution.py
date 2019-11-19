from crawler.crawler import Crawler
import argparse


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-t", help="crawl type")
	parser.add_argument("-mt", help="execution maximum time", default=0)
	parser.add_argument("-st", help="execution interval", default=0)
	args = parser.parse_args()
	if args:
		Crawler().run(args.t, args.mt, args.st)