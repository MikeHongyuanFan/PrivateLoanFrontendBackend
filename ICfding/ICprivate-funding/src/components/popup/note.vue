<template>
    <div class="popup">
        <div class="popup_title">
            <h1>Notes</h1>
            <div class="close">
                <!-- <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleMinimize"><Minus /></el-icon> -->
                <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleClose"><Close /></el-icon>                    
            </div>
        </div>
        <el-scrollbar>
            <div class="form">
                <button @click="add = true">
                    <el-icon :size="20" color="#FFF"><CirclePlus /></el-icon>
                    Add note
                </button>
                <div class="add" v-if="add === true">
                    <div class="title">
                        <p>Add New Note</p>
                        <el-icon :size="20" style="cursor: pointer; color: #384144;" @click="add = false"><Close /></el-icon>
                    </div>
                    <div class="form_content">
                        <div class="line">
                            <span>To:</span>
                            <el-select v-model="addData.assigned_to">
                                <el-option
                                    v-for="item in assign"
                                    :key="item.id"
                                    :label="item.first_name"
                                    :value="item.id"
                                />
                            </el-select>
                        </div>
                        <div class="line">
                            <span>Reminder Date:</span>
                            <el-date-picker
                                v-model="addData.remind_date"
                                type="date"
                                placeholder="Pick a day"
                            />
                        </div>
                        <div class="line">
                            <span>Subject:</span>
                            <el-input v-model="addData.title" />
                        </div> 
                        <el-input v-model="addData.content" type="textarea" placeholder="Type here..." />
                        <div class="buttons">
                            <button @click="handleAdd">Add Note</button>
                        </div>                   
                    </div>
                </div>
                <div v-for="(note, index) in notes" :key="index" class="add">
                    <div class="title">
                        <p>Noted By {{ note.created_by_name }}</p>
                        <p style="font-weight: 400;">{{ note.created_at?.split('T')[0] }}</p>
                    </div>
                    <div class="form_content">
                        <h2>Subject: {{ note.title }}</h2>
                        <p style="font-weight: 400;">{{ note.content }}</p>
                    </div>
                </div>
            </div>
        </el-scrollbar>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import { api } from '@/api'

    const { id } = defineProps({
        id: String
    })

    const notes = ref([])
    const add = ref(false)
    const addData = ref({
        title: "",
        content: "",
        remind_date: "",
        application: id,
        borrower: null,
        assigned_to: null
    })
    const assign = ref([])
    const emit = defineEmits(['close', 'minimize'])

    onMounted(() => {
        getNotes()
        getUsers()
    })

    const handleClose = () => {
        emit('close')
    }
    // const handleMinimize = () => {
    //     emit('minimize')
    // }
    const getNotes = async () => {
        const [err, res] = await api.notes()
        if (!err) {            
            notes.value = res.results
            console.log(notes.value);
        } else {
            console.log(err)
        }
    }
    const getUsers = async () => {
        const [err, res] = await api.users()
        if (!err) {            
            assign.value = res.results.filter(item => 
                item.role === 'admin' || item.role === 'bd'
            )
            console.log(assign.value);
        } else {
            console.log(err)
        }
    }
    const handleAdd = async () => {
        const [err, res] = await api.addNote(addData.value)
        if (!err) {
            console.log(res);
            add.value = false
        } else {
            console.log(err)
        }
    }
</script>

<style scoped>
    .popup {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        display: flex;
        flex-direction: column;
        background: white;
        border: none;
        box-shadow: -8px -1px 9.3px 0px rgba(202, 202, 202, 0.16);
        width: 35%;
        height: 100vh;
        overflow: hidden;
        z-index: 1000;
    }
    .popup_title {
        width: 100%;
        padding: 20px 10px;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1.5px solid var(--Line, #E1E1E1);
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 1.1rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    .close {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 20px;
    }
    .form {
        padding: 10px 15px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    button {
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid #E8EBEE;
        background: #2984DE;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        gap: 5px;
        outline: none;
        color: #FFF;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
    button:hover {
        background: #1F63A9;
    }
    .add {
        display: flex;
        flex-direction: column;
        border-radius: 8px;
        border: 1.5px solid #E8EBEE;
        overflow: hidden;        
    }
    .title {
        padding: 10px;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1.5px solid #E8EBEE;
        background: #F8F8F8;
    }
    p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
        margin: 0;
    }
    .form_content {
        padding: 15px 10px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    .line {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
    }
    span {
        color: #7A858E;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 400;
        line-height: normal;
        margin: 0;
    }
    .buttons {
        display: flex;
        flex-direction: row;
        justify-content: end;
        align-items: center;
    }
    h2 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: normal;
        margin: 0;
    }
</style>