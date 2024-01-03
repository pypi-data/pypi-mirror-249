build:
	maturin build --target-dir=./target --out=./target

install:
	make build
	pip install .

install-cli:
	cd cli
	pip install .
	cd ..

build-release:
	maturin build --release --strip --target-dir=./target --out=./target

clean:
	cargo clean

fmt:
	cargo fmt

lint:
	cargo clippy 

lint-fix-py:
	python -m black raftify.pyi
	python -m black **/*.py

publish:
	make build-release
	maturin publish --out=./target
