<template>
    <div class="login">
        <div class="login-info">
            <div class="user-info">
                <img class="logo" src="/src/assets/logo.png" alt="logo" />
                <div class="title">Welcome to Starx Private Loan Demo</div>
                <div class="tips">Use your email address to login</div>
                <el-form ref="ruleFormRef" :model="user" status-icon :rules="rules">
                    <el-form-item label="" prop="email">
                        <div class="item">
                            <el-input v-model="user.email" placeholder="Enter your eamil" />
                        </div>
                    </el-form-item>
                    <el-form-item label="" prop="password">
                        <div class="item">
                            <el-input v-model="user.password" :type="showPassword ? 'text' : 'password'"
                                placeholder="Enter your password">
                                <template #suffix>
                                    <el-icon class="view-icon" size="20" @click="() => showPassword = !showPassword">
                                        <View />
                                    </el-icon>
                                </template>
                            </el-input>
                        </div>
                    </el-form-item>
                    <el-form-item label="" prop="checkPass">
                        <div class="item">
                            <el-checkbox v-model="remember" label="Remember Password" />
                        </div>
                    </el-form-item>
                    <el-form-item>
                        <div class="item">
                            <el-button class="btn" @click="login">login</el-button>
                        </div>
                    </el-form-item>
                </el-form>
                <div class="forget">Forget Password?</div>
            </div>
            <img class="right-img" src="/src/assets/login_image.png" alt="logo" />
        </div>
    </div>

</template>

<script setup>
import { reactive, onMounted, ref } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { View } from '@element-plus/icons-vue'
import useSystem from '@/hooks/useSystem'

const router = useRouter()
const { setUserInfo, logOut } = useSystem()

const user = reactive({
    email: '',
    password: ''
})

const remember = ref(false)

const showPassword = ref(false)
const ruleFormRef = ref()
const rules = reactive({
    email: [
        { required: true, message: 'Please input Email', trigger: 'blur' },
    ],
    password: [
        { required: true, message: 'Please input Password', trigger: 'blur', },
    ]
})

onMounted(() => {
    logOut()
    setLoginUser()
})


const login = async () => {
    if (!ruleFormRef.value) return
    await ruleFormRef.value.validate(async (valid, fields) => {
        if (valid) {
            const [err, res] = await api.login(user)
            if (!err) {
                if (remember.value) {
                    localStorage.setItem('login', JSON.stringify(user))
                } else {
                    localStorage.removeItem('login')
                }
                setUserInfo(res)
                router.replace('/')
            }
        } else {
            console.log('error submit!', fields)
        }
    })
}

function setLoginUser() {
    const loginUser = localStorage.getItem('login')
    if (loginUser) {
        const userLoginInfo = JSON.parse(loginUser)
        user.email = userLoginInfo.email
        user.password = userLoginInfo.password
        remember.value = true
    }
}
</script>

<style lang="scss" scoped>
.login {
    width: 100vw;
    height: 100vh;

    .login-info {
        display: flex;
        align-items: center;

        .user-info {
            width: 50%;
            background: #fff;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            .logo {
                width: 120px;
                height: 39px;
            }

            .title {
                font-family: Inter;
                font-weight: 700;
                font-size: 18px;
                color: #384144;
                padding: 20px 0 10px;
            }

            .tips {
                font-family: Inter;
                font-weight: 400;
                font-size: 14px;
                color: #7A858E;
                padding: 0 0 20px;
            }

            .view-icon {
                cursor: pointer;
                color: #7A858E;
            }

            .item {
                display: flex;
                align-items: center;
                width: 330px;
                height: 36px;

                .btn {
                    width: 100%;
                    height: 36px;
                    background: #384144;
                    font-family: Inter;
                    font-weight: 500;
                    font-size: 16px;
                    color: #fff;
                    border-radius: 8px;
                }
            }

            .item+.item {
                margin-top: 10px;
            }

            .forget {
                font-family: Inter;
                font-weight: 400;
                font-size: 12px;
                line-height: 100%;
                letter-spacing: 0%;
                text-decoration: underline;
                text-decoration-style: solid;
                // text-decoration-offset: 0%;
                text-decoration-thickness: 0%;
                text-decoration-skip-ink: auto;
                color: #7A858E;
                cursor: pointer;
            }
        }

        .right-img {
            width: 50%;
            display: block;
            height: 100vh;
        }
    }
}
</style>