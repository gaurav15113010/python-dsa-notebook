import asyncio

suppliers = [
    "supplier_1",
    "supplier_2",
    "supplier_3",
    "supplier_4",
    "supplier_5",
    "supplier_6",
    "supplier_7",
    "supplier_8",
    "supplier_9",
    "supplier_10",
]

semaphore = asyncio.Semaphore(3) # Limit to 3 concurrent tasks

async def process_supplier(supplier):
    async with semaphore:
        print(f"Processing {supplier}...")
        await asyncio.sleep(1)
        print(f"Processing completed for : {supplier}")

async def main(suppliers:list):
    await asyncio.gather(
        *(process_supplier(supp) for supp in suppliers       # * used here to unpack it, else, this for loop output will be like an generator
    ))

asyncio.run(main(suppliers))


