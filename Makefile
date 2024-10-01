all: dfu_all/dfu.py
	cp license.txt dfu_all

PYSRC =	nordicsemi/dfu/intelhex/__init__.py \
		nordicsemi/dfu/intelhex/compat.py \
		nordicsemi/dfu/intelhex/getsizeof.py \
		nordicsemi/dfu/crc16.py \
		nordicsemi/dfu/dfu_transport.py \
		nordicsemi/dfu/dfu_transport_serial.py \
		nordicsemi/dfu/dfu_transport_ble.py \
		nordicsemi/dfu/init_packet.py \
		nordicsemi/dfu/manifest.py \
		nordicsemi/dfu/nrfhex.py \
		nordicsemi/dfu/signing.py \
		nordicsemi/dfu/dfu.py \
		nordicsemi/dfu/exceptions.py \
		nordicsemi/dfu/__init__.py \
		nordicsemi/dfu/model.py \
		nordicsemi/dfu/package.py \
		nordicsemi/dfu/util.py
		
test: dfu_all/dfu.py dfu_test.py
	python dfu_test.py

dfu_all/dfu.py: $(PYSRC)
	mkdir -p dfu_all
	cat $(PYSRC) | grep -v "from dfu[\.a-z0-9_]* import" |  grep -v "from \.[\.a-z0-9_]* import"  | perl -pe 's/(^|[^"])intelhex\.($$|[^"])/$$1$$2/g' > dfu_all/dfu.py

clean:
	rm -Rf dfu_all
