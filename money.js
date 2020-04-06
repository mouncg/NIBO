const nitrotype = require('nitrotype');
PWD = 'yeet';
UNAME = 'lmao';
UID = '42052507'; // Eppyforce
data = ({
    data: {
        amount: 100000,
        password: PWD
    }
});

SYSARGS = ({
    uname: process.argv[2].toString(),
    pwd: process.argv[3].toString(),
    amo: process.argv[4],
    uid: process.argv[5].toString()
});
SYSARGS.amo = parseInt(SYSARGS.amo);
//UNAME, PWD, data.data.amount, UID = SYSARGS.uname, SYSARGS.pwd, SYSARGS.amo, SYSARGS.uid;
UNAME = SYSARGS.uname;
PWD = SYSARGS.pwd;
data.data.amount = SYSARGS.amo;
UID = SYSARGS.uid;

const client = nitrotype({ username: UNAME, password: PWD });
function print(text){
console.log(text)
}
//print(SYSARGS);
//print(client);

(async () => {
    await client.login();
    const res = await client.get('rewards/daily');
    console.log(res);
    const resTWO = await client.post('friends/' + UID + '/sendcash', data);
    console.log(resTWO)
// Output: { success: true, data: { reward: true, next: 75600, type: 'money', value: 30000 } }
})();