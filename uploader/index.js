const Arweave = require("arweave");
const fs = require("fs");

const arweave = Arweave.init({
    host: 'arweave.net',
    port: 443,
    protocol: 'https'
});

(async() => {
    for (var i = 8452; i < 8888; i++) {
        let key = await arweave.wallets.generate();
        
        let transaction = await arweave.createTransaction({
            data: Buffer.from(fs.readFileSync(`../output/${i}.png`))
        }, key);
        
        transaction.addTag('Content-Type', 'image/png');
        
        await arweave.transactions.sign(transaction, key);
        
        let uploader = await arweave.transactions.getUploader(transaction);
        
        while (!uploader.isComplete) {
            await uploader.uploadChunk();
            console.log(`${uploader.pctComplete}% complete, ${uploader.uploadedChunks}/${uploader.totalChunks} ${transaction.id}`);
            fs.writeFileSync(`./arweave_ids/${i}`, transaction.id);
        }
    }
})();