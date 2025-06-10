import { getCurrentInstance, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

export function useLocale() {
  const { t, locale } = useI18n()

  /* getCurrentInstance()可以用来获取当前组件实例 */
  const current = getCurrentInstance()?.appContext.config.globalProperties

  // 根据状态，切换国际化
  const handleLanguageChange = (val) => {
    current.$i18n.locale = val
    window.localStorage.setItem('lang', val)
    // console.log(current.$i18n.locale)
  }

  const langStatus = ref(false)
  const lang = ref('en')
  const langStr = locale.value
  langStatus.value = langStr.includes('zh')
  lang.value = langStatus.value ? 'cn' : 'en'

  watch(
    () => locale.value,
    (val) => {
      langStatus.value = val.includes('zh')
      lang.value = langStatus.value ? 'cn' : 'en'
    }
  )

  return { t, handleLanguageChange, langStatus, lang }
}
