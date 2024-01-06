import typer

app=typer.Typer()


@app.command()
def main(batch_size:int =32, lr:float = 0.001, momentum:float=0.089):
    print(f"I am doing something using batch_size= {batch_size},lr={lr},momentum={momentum}")
    if lr>0.1:
        print(f"too high lr {lr} reduce it")