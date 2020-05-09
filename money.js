const nitrotype = require('nitrotype');


SYSARGS = ({
    uname: process.argv[2].toString(),
    pwd: process.argv[3].toString(),
    amo: parseInt(process.argv[4]),
    uid: process.argv[5].toString()
});
data = ({
    data: {
        amount: SYSARGS.amo,
        password: SYSARGS.pwd
    }
});

const client = nitrotype({ username: SYSARGS.uname, password: SYSARGS.pwd });
function print(text){
console.log(text)
}

(async () => {
    await client.login();
    const res = await client.get('rewards/daily');
    console.log(res);
    const resTWO = await client.post('friends/' + SYSARGS.uid + '/sendcash', data);
    console.log(resTWO)
// Output: { success: true, data: { reward: true, next: 75600, type: 'money', value: 30000 } }
})();