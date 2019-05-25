#include "inc/hw_ints.h"  //NVIC birimi
#include "inc/hw_memmap.h" //Hafıza birimi portF için
#include "inc/hw_types.h" //
#include "driverlib/sysctl.h" //Sistem Clock 
#include "driverlib/interrupt.h" //Kesme birimleri
#include "driverlib/gpio.h"   //Kullanacağımız gpio birimleri
#include "driverlib/timer.h"

// https://www.mcu-turkey.com/stellaris-launchpad-timer-pwm/

int main(void)
{
	unsigned long Period; //Timer için kullancağımız değişken
	
	SysCtlClockSet(SYSCTL_SYSDIV_5|SYSCTL_USE_PLL|SYSCTL_XTAL_16MHZ|SYSCTL_OSC_MAIN);//40 MHZ'lik clock sinyali
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF); //PortF Tanımlaması
	
	GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3); //PortF^teki gpiolar
	
	SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1); //Timer1 aktif ediliyor
	
	TimerConfigure(TIMER1_BASE, TIMER_CFG_32_BIT_PER);//32 Bit periyodik timerı kullanıyoruz   
	
	Period=(SysCtlClockGet() / 10) / 2; // %50 dutycycle ve 10HZ lik bir sinyali Period değişkenine atadık
	
	TimerLoadSet(TIMER1_BASE, TIMER_A, Period -1);//Timer birimine period değişkenini okutuyoruz
	
	IntEnable(INT_TIMER1A);//Kesmeler aktif
	TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
	
	IntMasterEnable();//Master olarak kullanacağız
	TimerEnable(TIMER1_BASE, TIMER_A);//Timer1 Aktif
 
	while(1)
	{
	}
}

void Timer1IntHandler(void)//Timer Fonksiyonu
{
	TimerIntClear(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
	
	if(GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_3))
	{
		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3,0);
	}
	else
	{
		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_3, 8);
	}
}
